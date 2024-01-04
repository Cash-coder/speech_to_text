from utils.lib.driver import create_normal_driver, grant_permissions, close_driver
from utils.config import TARGET_URLS, XPATH_LIBRARY
from utils.lib.text import get_text, paste_text
from selenium.webdriver.common.by import By
from time import sleep
import logging

logging.basicConfig(filename='logs.log', level=logging.DEBUG)


def press_record_btn(d):
    sleep(2)
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()
    print('\nProgram running\n')


def run():

    d = create_normal_driver()

    d.get(TARGET_URLS['dictation_url'])

    grant_permissions(d)  # microphone, geo location, camera

    # open second tab to get grammar improvement suggestions
    # open_second_tab(d, TARGET_URLS['grammar_url']) # open grammar tab
    # switch_to_american_english(d)

    press_record_btn(d)

    while True:
        text = get_text(d)

        paste_text(text)


if __name__ == '__main__':
    run()
