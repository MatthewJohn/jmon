
from jmon import app
import jmon.tasks.perform_check
import jmon.tasks.update_check_schedules
import jmon.tasks.clean_orphaned_checks
import jmon.tasks.remove_expired_runs
import jmon.tasks.update_artifact_lifecycle_rules
import jmon.tasks.check_queue_timeouts


# Register tasks with celery
app.task(bind=True)(jmon.tasks.perform_check.perform_check)
app.task(jmon.tasks.update_check_schedules.update_check_schedules)
app.task(jmon.tasks.clean_orphaned_checks.clean_orphaned_checks)
app.task(jmon.tasks.remove_expired_runs.remove_expired_runs)
app.task(jmon.tasks.update_artifact_lifecycle_rules.update_artifact_lifecycle_rules)
app.task(jmon.tasks.check_queue_timeouts.check_queue_timeouts)

# Set pre-fetch multiplier to 1 so that workers only pull the message
# they are currently working on
app.conf.worker_prefetch_multiplier = 1
