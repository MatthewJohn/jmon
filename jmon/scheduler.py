

from time import sleep
from jmon import app
import jmon.config
import jmon.models


# Setup beat schedules
app.conf.beat_schedule = {
    # Update check schedules
    'update_check_schedules': {
        'task': 'jmon.tasks.update_check_schedules.update_check_schedules',
        'schedule': 120.0,
        'args': []
    },
}
