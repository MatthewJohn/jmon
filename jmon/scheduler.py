

from time import sleep
from jmon import app
import jmon.config
import jmon.models


# Setup beat schedules
app.conf.beat_schedule = {
    # Update check schedules
    'update_check_schedules': {
        'task': 'jmon.tasks.update_check_schedules.update_check_schedules',
        'schedule': 30.0,
        'args': []
    },
    # Clean orphaned checks every 12 hours
    'clean_orphaned_checks': {
        'task': 'jmon.tasks.clean_orphaned_checks.clean_orphaned_checks',
        'schedule': 43200.0,
        'args': []
    }
}
