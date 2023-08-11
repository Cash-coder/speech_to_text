from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
import pyperclip
import keyboard
import pyautogui
# from selenium.webdriver import Keys
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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

    print('driver created')

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


def record_and_paste(d):

    # start recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    text = get_text(d)

    paste_text(text)

    # stop recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    print_grammar_correction(d, text)


def print_grammar_correction(d, text):

    # open grammar page
    d.get(TARGET_URLS['grammar_url'])

    # paste text
    d.find_element(By.XPATH, '//textarea').send_keys(text)

    # wait for grammar correction
    sleep(1)

    # get corrected text
    corrected_text = d.find_element(By.XPATH, '//textarea').text

    # paste corrected text
    paste_text(corrected_text)

    # go back to dictation page
    d.get(TARGET_URLS['dictation_url'])


def get_text(d):
    tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
    wait_until_started_to_change(d, XPATH_LIBRARY['text_mirror'])
    text_chain = []

    while True:

        sleep(0.1)
        tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
        text_chain.append(tm.text)

        if tm.text == '':  # when input recording ends, it sets to ''
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
            print('element not changed after ' + str(n) + ' iterations')
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


def open_tabs(d):
    d.execute_script("window.open('');")
    d.switch_to.window(d.window_handles[1])
    d.get(TARGET_URLS['grammar_url'])
    d.switch_to.window(d.window_handles[0])


def run():
    d = create_driver()

    open_tabs(d)  # open dictation and grammar tabs

    d.get(TARGET_URLS['dictation_url'])

    grant_permissions(d)  # microphone, geo location, camera

    keyboard.add_hotkey('ctrl+shift+ñ', lambda: record_and_paste(d))

    while True:
        try:
            keyboard.wait('esc')  # trigger shortcut
        except Exception as e:
            print(e)
            close_driver(d)
            break


if __name__ == '__main__':
    run()
