
from time import sleep

from pyvirtualdisplay import Display
import selenium
from selenium.webdriver.common.by import By


class Runner:

    def perform_check(self, config):
        display_instance = Display(visible=0, size=(1920, 1080))
        display_instance.start()
        selenium_instance = selenium.webdriver.Firefox()
        selenium_instance.delete_all_cookies()
        selenium_instance.implicitly_wait(1)

        try:

            def find_element(child_config, parent_element=None):
                """"""
                if parent_element is None:
                    parent_element = selenium_instance
                child = selenium_instance
                if child_config.get('id'):
                    child = parent_element.find_element(By.ID, child_config.get('id'))
                if child_config.get('class'):
                    child = parent_element.find_element(By.CLASS_NAME, child_config.get('class'))

                # Recursively find any child elements
                if child_config.get('find'):
                    child = find_element(child_config.get('find'), parent_element=child)
                return child

            def retry(fnc):
                for itx in range(3):
                    try:
                        fnc()
                        return
                    except Exception:
                        if itx == 2:
                            raise
                        sleep(1)

            for action in config.get('steps'):
                if action.get('goto'):
                    selenium_instance.get(action.get('goto'))

                if action.get('check'):
                    checks = action.get('check')
                    if checks.get('title'):
                        assert selenium_instance.title == checks.get('title')
                    if checks.get('url'):
                        assert selenium_instance.current_url == checks.get('url')

                if action.get('type'):
                    find_element(action.get('type')).send_keys(action.get('type').get('text'))

                if action.get('click'):
                    find_element(action.get('click')).click()
        finally:
            selenium_instance.quit()
            display_instance.stop()
