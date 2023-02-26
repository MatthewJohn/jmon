
import argparse
from jmon import app
from jmon.client_type import ClientType
import jmon.tasks.perform_check
import jmon.tasks.update_check_schedules
import jmon.tasks.clean_orphaned_checks


# Register tasks with celery
app.task(bind=True)(jmon.tasks.perform_check.perform_check)
app.task(jmon.tasks.update_check_schedules.update_check_schedules)
app.task(jmon.tasks.clean_orphaned_checks.clean_orphaned_checks)
