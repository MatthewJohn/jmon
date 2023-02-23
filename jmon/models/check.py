

import sqlalchemy

import yaml
import json
from jmon.client_type import ClientType

import jmon.database
import jmon.config
from jmon.errors import CheckCreateError
import jmon.models.run
from jmon.steps.root_step import RootStep
import jmon.run


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

        return instance


    __tablename__ = 'check'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(jmon.database.Database.GeneralString, primary_key=True)
    screenshot_on_error = sqlalchemy.Column(sqlalchemy.Boolean)
    interval = sqlalchemy.Column(sqlalchemy.Integer)
    client = sqlalchemy.Column(sqlalchemy.Enum(ClientType), default=None)
    _steps = sqlalchemy.Column(jmon.database.Database.LargeString, name="steps")

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
        session = jmon.database.Database.get_session()
        session.delete(self)
        session.commit()

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
