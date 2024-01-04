from tab import switch_tabs
from time import sleep
from selenium.webdriver.common.by import By


def print_grammar_correction(d, text):
    switch_tabs(d)

    # send text
    # include xpath in path library Json
    d.find_element(By.XPATH, '//d-textarea[contains(@class, "lmt__source_textarea")]').send_keys(text)

    # DEBT: create dynamic wait until the icon of 'working' starts and dissappears
    sleep(1.5)

    # copy text
    d.find_element(By.XPATH, '//d-textarea[contains(@class, "lmt__textarea lmt__target_textarea")]').click()

    # print in CLI

    # clean input field for next grammar correction

    switch_tabs(d)


def switch_to_american_english(d):
    switch_tabs(d)

    # click button to switch language
    d.find_element(By.XPATH, '//button[@id="headlessui-listbox-button-10"]').click()

    sleep(0.5)

    # click in american
    d.find_element(By.XPATH, '//span[contains(text(), "American")]').click()
