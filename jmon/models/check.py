

import sqlalchemy

from redbeat import RedBeatSchedulerEntry
import yaml
import json
import celery

from jmon.client_type import ClientType
from jmon import app
import jmon.database
import jmon.config
from jmon.errors import CheckCreateError
import jmon.models.run
from jmon.steps.root_step import RootStep
import jmon.run
from jmon.logger import logger


class Check(jmon.database.Base):

    @classmethod
    def get_all(cls):
        """Get all checks"""
        session = jmon.database.Database.get_session()
        return session.query(cls).all()

    @classmethod
    def get_by_name(cls, name):
        """Get all checks"""
        session = jmon.database.Database.get_session()
        return session.query(cls).filter(cls.name==name).first()

    @classmethod
    def from_yaml(cls, yml):
        """Return instance of class from check yaml"""
        try:
            content = yaml.safe_load(yml)
        except Exception as exc:
            raise CheckCreateError('Invalid YAML')

        if type(content) is not dict:
            raise CheckCreateError("YAML must be a dictionary")

        if not (name := content.get("name")):
            raise CheckCreateError("No name defined for check")

        if not (steps := content.get("steps")):
            raise CheckCreateError("No steps defined for check")

        # Check for existing steps with the same name
        session = jmon.database.Database.get_session()

        instance = session.query(cls).filter(cls.name==name).first()
        # Create new instance of check, if it doesn't exist
        if not instance:
            instance = cls(name=name)

        instance.steps = steps
        instance.screenshot_on_error = content.get("screenshot_on_error")

        if client_type := content.get("client"):
            try:
                instance.client = ClientType(client_type)
            except ValueError:
                raise CheckCreateError("Invalid client type")
        else:
            instance.client = None
        instance.interval = int(content.get("interval", 0))

        session.add(instance)
        session.commit()

        # Enable check by default, or if directed to
        if content.get("enable", True):
            instance.enable()
        else:
            instance.disable()

        return instance


    __tablename__ = 'check'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(jmon.database.Database.GeneralString, primary_key=True)
    screenshot_on_error = sqlalchemy.Column(sqlalchemy.Boolean)
    interval = sqlalchemy.Column(sqlalchemy.Integer)
    client = sqlalchemy.Column(sqlalchemy.Enum(ClientType), default=None)
    _steps = sqlalchemy.Column(jmon.database.Database.LargeString, name="steps")
    enabled = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    @property
    def steps(self):
        """Return steps dictionary"""
        return json.loads(self._steps)

    @steps.setter
    def steps(self, value):
        """Set steps in database"""
        self._steps = json.dumps(value)

    @property
    def should_screenshot_on_error(self):
        """Whether a screenshot should be taken on error"""
        # Return confinguration for check, if available
        if self.screenshot_on_error is not None:
            return self.screenshot_on_error

        # Return default config for whether to screenshot on failure
        return jmon.config.Config.get().SCREENSHOT_ON_FAILURE_DEFAULT

    def delete(self):
        """Delete check"""

        # Delete from schedule, if it exists
        try:
            entry = RedBeatSchedulerEntry.from_key(key=f"redbeat:check_{self.name}", app=app)
            entry.delete()
        except KeyError:
            pass

        # Delete from database
        session = jmon.database.Database.get_session()
        session.delete(self)
        session.commit()

    def enable(self):
        """Enable the check"""
        # Update DB row
        session = jmon.database.Database.get_session()
        self.enabled = False
        session.add(self)
        session.commit()

        self.upsert_schedule()

    def disable(self):
        """Disable the check"""
        self.delete_schedule()

        # Update DB row
        session = jmon.database.Database.get_session()
        self.enabled = False
        session.add(self)
        session.commit()

    def upsert_schedule(self):
        """Register or update schedule"""
        headers = self.task_headers
        if not headers:
            logger.warn(f"Check does not have any compatible client types: {self.name}")
            return

        options = {
            'headers': headers,
            'exchange': 'check'
        }

        interval_seconds = self.get_interval()
        interval = celery.schedules.schedule(run_every=interval_seconds)

        key = f'check_{self.name}'

        needs_to_save = False
        reschedule = False
        try:
            entry = RedBeatSchedulerEntry.from_key(key=f"redbeat:{key}", app=app)
            if (entry.schedule.run_every != interval.run_every or
                    entry.options.get('headers') != options['headers'] or
                    entry.options.get('exchange') != options['exchange']):
                # Update interval and set directive to save
                entry.interval = interval
                entry.options.update(options)

                needs_to_save = True

                # Re-schedule to allow previously scheduled
                # runs to be rescheduled
                reschedule = True

        except KeyError:
            # If it does not exist, create new entry
            entry = RedBeatSchedulerEntry(
                key,
                'jmon.tasks.perform_check.perform_check',
                interval,
                args=[self.name],
                app=app,
                options=options
            )
            needs_to_save = True

        if needs_to_save:
            entry.save()
            if reschedule:
                entry.reschedule()

    def delete_schedule(self):
        """De-register from schedule"""
        # Delete from schedule, if it exists
        try:
            entry = RedBeatSchedulerEntry.from_key(key=f"redbeat:check_{self.name}", app=app)
            entry.delete()
        except KeyError:
            pass

    def get_result_key(self):
        """Get redis key prefix for results."""
        return f"jmon_run_result_{self.name}_"

    def get_interval(self):
        """Return interval of check, based on custom definition, global min/max and default interval"""
        config = jmon.config.Config.get()
        # If the interval has been set on the check
        if self.interval != 0:
            return max(min(self.interval, config.MAX_CHECK_INTERVAL), config.MIN_CHECK_INTERVAL)

        # Return default check interval
        return config.DEFAULT_CHECK_INTERVAL

    def get_supported_clients(self):
        """Get supported clients"""
        supported_clients = ClientType.get_all()
        if self.client:
            supported_clients = [self.client]

        root_step = RootStep(run=jmon.run.Run(check=self), config=self.steps, parent=None)

        supported_clients = root_step.get_supported_clients(supported_clients)
        return supported_clients

    @property
    def task_headers(self):
        """Get queue for task"""
        supported_clients = self.get_supported_clients()

        if not supported_clients:
            return None

        headers = {}

        if ClientType.REQUESTS in supported_clients:
            headers["requests"] = "true"
        if ClientType.BROWSER_CHROME in supported_clients:
            headers["chrome"] = "true"
        if ClientType.BROWSER_FIREFOX in supported_clients:
            headers["firefox"] = "true"
        return headers
