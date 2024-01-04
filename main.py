from selenium.webdriver.common.by import By
from time import sleep
import pyperclip
import keyboard
import pyautogui
import logging
# from selenium.common import WebDriverException
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys


logging.basicConfig(filename='logs', level=logging.DEBUG)

TARGET_URLS = {
    'dictation_url': 'https://speechnotes.co/dictate/',
    'grammar_url': 'https://www.deepl.com/write'
}

XPATH_LIBRARY = {
    'record_button': '//div[@id="start_button"]',
    'text_area': '//div[@id="output_box"]/textarea',
    'text_mirror': '//div[@id="mirror_container"]//div',
}


#  undetectable driver
def create_driver():
    import undetected_chromedriver as uc

    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless=new')
    options.add_argument("--no-default-browser-check")
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2
    })

    driver = uc.Chrome(options=options)

    logging.debug('driver created')

    return driver


def create_normal_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless=new')
    # opts.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)  #, options=chrome_options)
    return driver


def grant_permissions(d):
    d.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": TARGET_URLS['dictation_url'],
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )


def execute_iteration(d):

    # start recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    text = get_text(d)

    paste_text(text)

    # stop recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    # print_grammar_correction(d, text)


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


def get_text(d):
    tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
    wait_until_started_to_change(d, XPATH_LIBRARY['text_mirror'])
    text_chain = []

    while True:

        sleep(0.1)
        tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
        text_chain.append(tm.text)

        if tm.text == '':  # when input recording ends, it sets itself to ''
            # the last normally is '' -> [-2], unless only one word is said [-1]
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


def close_driver(d):
    d.close()
    d.quit()


def open_second_tab(d, url):
    d.execute_script(f'''window.open("{url}","_blank");''')


# def open_tabs(d):
#     d.execute_script("window.open('');")
#     d.switch_to.window(d.window_handles[1])
#     d.get(TARGET_URLS['grammar_url'])
#     d.switch_to.window(d.window_handles[0])

def switch_tabs(d):
    current_tab = d.current_window_handle

    # check all the tabs, switch to the one that differs from the current tab
    for tab in d.window_handles:
        if tab != current_tab:
            d.switch_to.window(tab)


def switch_to_american_english(d):
    switch_tabs(d)

    # click button to switch language
    d.find_element(By.XPATH, '//button[@id="headlessui-listbox-button-10"]').click()

    sleep(0.5)

    # click in american
    d.find_element(By.XPATH, '//span[contains(text(), "American")]').click()


def press_record_btn(d):
    sleep(2)
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()
    print('\nProgram running\n')


def run():
    # d = create_driver()
    d = create_normal_driver()

    d.get(TARGET_URLS['dictation_url'])

    grant_permissions(d)  # microphone, geo location, camera

    # open_second_tab(d, TARGET_URLS['grammar_url']) # open grammar tab

    # switch_to_american_english(d)

    press_record_btn(d)

    keyboard.add_hotkey('ctrl+shift+ñ', lambda: execute_iteration(d))

    while True:
        try:
            keyboard.wait('esc')  # trigger shortcut
        except Exception as e:
            print(e)
            close_driver(d)
            break


if __name__ == '__main__':
    run()
