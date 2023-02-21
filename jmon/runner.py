
from time import sleep

from pyvirtualdisplay import Display
import selenium
from selenium.webdriver.chrome.options import Options

from jmon.client_type import ClientType
from jmon.step_state import RequestsStepState, SeleniumStepState
from jmon.step_status import StepStatus
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
    def get_selenium_instance(client_type):
        kwargs = {}
        browser_class = None

        if client_type is ClientType.BROWSER_FIREFOX:
            browser_class = selenium.webdriver.Firefox
        elif client_type is ClientType.BROWSER_CHROME:
            browser_class = selenium.webdriver.Chrome
            opts = Options()
            opts.binary_location = "/usr/bin/chromium-browser"
            kwargs["chrome_options"] = opts
        else:
            raise Exception(f"Unrecognised selenium ClientType: {client_type}")

        # Get display
        Runner.get_display()

        # If runner selenium is the wrong type, close
        # down the old one
        if Runner.SELENIUM_INSTANCE and not isinstance(Runner.SELENIUM_INSTANCE, browser_class):
            Runner.SELENIUM_INSTANCE.quit()
            Runner.SELENIUM_INSTANCE = None

        if Runner.SELENIUM_INSTANCE is None:
            Runner.SELENIUM_INSTANCE = browser_class(**kwargs)
            Runner.SELENIUM_INSTANCE.implicitly_wait(1)

        # Remove cookies before starting
        Runner.SELENIUM_INSTANCE.delete_all_cookies()

        return Runner.SELENIUM_INSTANCE

    def perform_check(self, run):
        """Setup selenium and perform checks"""
        supported_clients = run.check.get_supported_clients()

        run.logger.info(f"Supported clients: {supported_clients}")
        if not supported_clients:
            raise Exception("There are no supported clients for check")
        client_type = supported_clients[0]
        run.logger.info(f"Using client: {client_type}")

        if client_type is ClientType.REQUESTS:
            # Execute using requests
            status = run.root_step.execute(
                execution_method='execute_requests',
                state=RequestsStepState(None)
            )
        elif client_type in [ClientType.BROWSER_FIREFOX, ClientType.BROWSER_CHROME]:

            selenium_instance = self.get_selenium_instance(client_type)

            root_state = SeleniumStepState(selenium_instance=selenium_instance, element=selenium_instance)

            status = run.root_step.execute(
                execution_method='execute_selenium',
                state=root_state
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
                    state=root_state
                )
        else:
            raise Exception(f"Unknown client: {client_type}")

        return status
