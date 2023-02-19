
from time import sleep

from pyvirtualdisplay import Display
import selenium
from jmon.client_type import ClientType
from jmon.step_status import StepStatus

from jmon.steps import RootStep
from jmon.steps.actions.screenshot_action import ScreenshotAction


class Runner:
    """Execute run"""

    DISPLAY = None
    SELENIUM_INSTANCE = None

    @staticmethod
    def get_display():
        if Runner.DISPLAY is None:
            Runner.DISPLAY = Display(visible=0, size=(1920, 1080))
            Runner.DISPLAY.start()
        return Runner.DISPLAY

    @staticmethod
    def get_selenium_instance():
        # Get display
        Runner.get_display()

        if Runner.SELENIUM_INSTANCE is None:
            Runner.SELENIUM_INSTANCE = selenium.webdriver.Firefox()
            Runner.SELENIUM_INSTANCE.implicitly_wait(1)
        Runner.SELENIUM_INSTANCE.delete_all_cookies()
        return Runner.SELENIUM_INSTANCE

    def perform_check(self, run):
        """Setup selenium and perform checks"""
        supported_clients = run.root_step.get_supported_clients([
            ClientType.REQUESTS,
            ClientType.BROWSER_FIREFOX
        ])

        run.logger.info(f"Supported clients: {supported_clients}")
        if not supported_clients:
            raise Exception("There are no supported clients for check")
        client_type = supported_clients[0]
        run.logger.info(f"Using client: {client_type}")

        if client_type is ClientType.REQUESTS:
            # Execute using requests
            _, status = run.root_step.execute(
                execution_method='execute_requests',
                element=None
            )
        elif client_type is ClientType.BROWSER_FIREFOX:
            selenium_instance = self.get_selenium_instance()
            _, status = run.root_step.execute(
                execution_method='execute_selenium',
                selenium_instance=selenium_instance,
                element=selenium_instance
            )

            if status is StepStatus.FAILED and run.check.should_screenshot_on_error:
                # Perform failure screenshot, if configured
                error_screenshot = ScreenshotAction(
                    run=run,
                    config="failure",
                    parent=run.root_step,
                    enable_log=False
                )
                error_screenshot.execute(
                    execution_method='execute_selenium',
                    selenium_instance=selenium_instance,
                    element=selenium_instance
                )
        else:
            raise Exception(f"Unknown client: {client_type}")

        return status
