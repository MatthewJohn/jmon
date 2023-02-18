
from time import sleep

from pyvirtualdisplay import Display
import selenium
from jmon.step_status import StepStatus

from jmon.steps import RootStep
from jmon.steps.actions.screenshot_action import ScreenshotAction


class Runner:
    """Execute run"""

    def perform_check(self, run):
        """Setup selenium and perform checks"""
        display_instance = Display(visible=0, size=(1920, 1080))
        display_instance.start()

        selenium_instance = selenium.webdriver.Firefox()
        selenium_instance.delete_all_cookies()
        selenium_instance.implicitly_wait(1)

        root_step = RootStep(run=run, config=run.check.steps, parent=None)
        status = StepStatus.FAILED
        try:
            _, status = root_step.execute(
                selenium_instance=selenium_instance,
                element=selenium_instance
            )

            if status is StepStatus.FAILED and run.check.should_screenshot_on_error:
                # Perform failure screenshot, if configured
                error_screenshot = ScreenshotAction(
                    run=run,
                    config="failure",
                    parent=root_step,
                    enable_log=False
                )
                error_screenshot.execute(
                    selenium_instance=selenium_instance,
                    element=selenium_instance
                )

        finally:

            selenium_instance.quit()
            display_instance.stop()

        return status
