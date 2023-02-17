
from time import sleep

from pyvirtualdisplay import Display
import selenium

from jmon.steps import RootStep
from jmon.steps.actions.screenshot_action import ScreenshotAction


class Runner:

    def perform_check(self, run):
        """Setup selenium and perform checks"""
        display_instance = Display(visible=0, size=(1920, 1080))
        display_instance.start()

        selenium_instance = selenium.webdriver.Firefox()
        selenium_instance.delete_all_cookies()
        selenium_instance.implicitly_wait(1)

        try:
            root_step = RootStep(run=run, config=run.check.steps)
            root_step.execute(
                selenium_instance=selenium_instance,
                element=selenium_instance
            )

        except:
            # Perform failure screenshot, if configured
            if run.check.should_screenshot_on_error:
                error_screenshot = ScreenshotAction(run=run, config="failure")
                error_screenshot.execute(
                    selenium_instance=selenium_instance,
                    element=selenium_instance)

        finally:

            selenium_instance.quit()
            display_instance.stop()
