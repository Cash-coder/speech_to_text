from selenium.webdriver.common.by import By
from ..config import XPATH_LIBRARY
from time import sleep
import logging
import pyperclip
import pyautogui


def get_text(d):

    tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])

    wait_until_started_to_change(d, XPATH_LIBRARY['text_mirror'])
    text_chain = []

    while True:

        sleep(0.1)
        tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
        text_chain.append(tm.text)

        # stop recording when stop speaking, return text
        if tm.text == '':  # when input recording ends, it sets itself to ''
            # the last normally is '' -> [-2], unless only one word is said, then is [-1]
            try:
                return text_chain[-2]
            except:
                return text_chain[-1]


def wait_until_started_to_change(d, xpath_element):
    n = 0
    while True:
        sleep(0.1)
        n += 1
        element = d.find_element(By.XPATH, xpath_element)
        if element.text != '':
            return
        elif n > 70:
            logging.debug('element not changed after ' + str(n) + ' iterations')
            return


def paste_text(text):
    # copy old clipboard to avoid the user from having the same text twice when pasting
    old_clipboard = pyperclip.paste()

    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')

    pyperclip.copy(old_clipboard)

