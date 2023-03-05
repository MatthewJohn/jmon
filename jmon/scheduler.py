

from jmon import app
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
    },
    # Clean expired results every hour
    'remove_expired_runs': {
        'task': 'jmon.tasks.remove_expired_runs.remove_expired_runs',
        'schedule': 3600.0,
        'args': []
    },
    # Set bucket policy on artifact storage bucket every day
    'update_artifact_lifecycle_rules': {
        'task': 'jmon.tasks.update_artifact_lifecycle_rules.update_artifact_lifecycle_rules',
        'schedule': 86400.0,
        'args': []
    },
    # Check for tasks that encountered a queue timeout
    'check_queue_timeouts': {
        'task': 'jmon.tasks.check_queue_timeouts.check_queue_timeouts',
        'schedule': 60.0,
        'args': []
    }
}
