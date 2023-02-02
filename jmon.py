#!python

import sys
from time import sleep

import yaml
from pyvirtualdisplay import Display
import selenium
from selenium.webdriver.common.by import By


with open(sys.argv[1], "r") as fh:
    config = yaml.load(fh, yaml.FullLoader)

print(config)

display_instance = Display(visible=0, size=(1920, 1080))
display_instance.start()
selenium_instance = selenium.webdriver.Firefox()
selenium_instance.delete_all_cookies()
selenium_instance.implicitly_wait(1)

def find_element(config, parent_element=None):
    """"""
    if parent_element is None:
        parent_element = selenium_instance
    child = selenium_instance
    if config.get('id'):
        child = parent_element.find_element(By.ID, config.get('id'))
    if config.get('class'):
        child = parent_element.find_element(By.CLASS_NAME, config.get('class'))

    # Recursively find any child elements
    if config.get('find'):
        child = find_element(config.get('find'), parent_element=child)
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

for action in config:
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
