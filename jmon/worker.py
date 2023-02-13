
from jmon import app
import jmon.tasks.perform_check
import jmon.tasks.update_check_schedules


# Register tasks with celery
app.task(jmon.tasks.perform_check.perform_check)
app.task(jmon.tasks.update_check_schedules.update_check_schedules)
