
import argparse
from jmon import app
from jmon.client_type import ClientType
import jmon.tasks.perform_check
import jmon.tasks.update_check_schedules


# Register tasks with celery
app.task(jmon.tasks.perform_check.perform_check)
app.task(jmon.tasks.update_check_schedules.update_check_schedules)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(__name__)
    parser.add_argument(
        '--client',
        nargs='+',
        choices=[client_type.value for client_type in ClientType]
    )

    worker = app.Worker(

    )
    worker.start()
