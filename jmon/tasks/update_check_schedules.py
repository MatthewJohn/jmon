
import celery.schedules
from redbeat import RedBeatSchedulerEntry

import jmon.models
import jmon.config
import jmon.database
from jmon import app
from jmon.logger import logger


def update_check_schedules():
    """Add task schedules for each check in database."""
    checks = jmon.models.Check.get_all()
    for check in checks:
        routing_key = check.routing_key
        if not routing_key:
            logger.warn(f"Check does not have any compatible client types: {check.name}")
            continue

        interval_seconds = check.get_interval()
        interval = celery.schedules.schedule(run_every=interval_seconds)

        key = f'check_{check.name}'
        print(f'Using routing key: {routing_key}')

        needs_to_save = False
        reschedule = False
        try:
            entry = RedBeatSchedulerEntry.from_key(key=f"redbeat:{key}", app=app)
            if entry.schedule.run_every != interval.run_every or entry.options.get('routing_key') != routing_key:
                # Update interval and set directive to save
                entry.interval = interval
                entry.options['routing_key'] = routing_key

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
                args=[check.name],
                app=app,
                options={
                    'routing_key': routing_key
                }                
            )
            needs_to_save = True

        if needs_to_save:
            entry.save()
            if reschedule:
                entry.reschedule()

    # Clear down session
    jmon.database.Database.clear_session()
