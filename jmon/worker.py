
import argparse
from jmon import app
from jmon.client_type import ClientType
import jmon.tasks.perform_check
import jmon.tasks.update_check_schedules
import jmon.tasks.clean_orphaned_checks
import jmon.tasks.remove_expired_runs
import jmon.tasks.update_artifact_lifecycle_rules


# Register tasks with celery
app.task(bind=True)(jmon.tasks.perform_check.perform_check)
app.task(jmon.tasks.update_check_schedules.update_check_schedules)
app.task(jmon.tasks.clean_orphaned_checks.clean_orphaned_checks)
app.task(jmon.tasks.remove_expired_runs.remove_expired_runs)
app.task(jmon.tasks.update_artifact_lifecycle_rules.update_artifact_lifecycle_rules)
