from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pyperclip
import subprocess
import keyboard
import pyautogui
import time


# should measure that rare text change
# use API
# -remove the a
# - with exec ?
# -sending chain as argument
# - con alt shift to back cursor to last position

TARGET_URL = 'https://speechnotes.co/dictate/'
XPATH_LIBRARY = {
    'record_button': '//div[@id="start_button"]',
    'text_area': '//div[@id="output_box"]/textarea'
}


def print_help():
    print(f'''This is a python selenium refresher: 
          d.get("https://en.wikipedia.org/wiki/Main_Page") 
          //tag[contains(@attribute, 'substring')]
          //div[contains(text(), 'Google')]"# actions = ActionChains(d)
            actions.send_keys(Keys.ENTER).perform()
            d.switch_to.active_element
            with open('f2.txt', 'w', encoding="utf-8") as f: f.write(d.page_source)
          
          How to use: 
          --f for find_element(By.XPATH, '//button')
          ie: --f target_xpath -> e = find_element(By.XPATH, '//target_xpath')
          --fs for find_elementS(By.XPATH, '//button'
          driver.find_elements(By.XPATH, '//button')
          
            
          ''')


def create_driver():
    import undetected_chromedriver as uc

    driver = uc.Chrome(headless=False, use_subprocess=False)

    return driver


def read_user_input():
    return input("Enter function to run, q for exit, h for help: ")


def execute_func(func):
    try:
        print("executing: " + func + "\n")
        exec(func, globals())  # globals used to allow to assign variables
    except Exception as e:
        print("\n" + str(e) + "\n")
        pass


def function_parser(func):
    if func.lower() in ("quit", "q", "exit"):
        return 'q'
    if func.lower() in ("help", "h"):
        print_help()
        return 'continue'

    # common function layout
    # if '--f' or '-f' in func.lower():
    #     try:
    #         xpath = func.split(' ')[1]
    #         func = f"d.find_element(By.XPATH, '{xpath}')"
    #
    #         print("\n xpath is: " + xpath, "\n", "function is: " + func + "\n")
    #
    #         return func
    #
    #     except Exception as e:
    #         print(e)
    #         pass

    return func


def execution_wheel(d):
    while True:

        function_to_execute = read_user_input()

        r = function_parser(function_to_execute)
        if r == 'q':  # if user input is q, exit
            close_driver(d)
            break
        elif r == 'continue':
            continue

        execute_func(r)


def grant_permissions():
    d.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": TARGET_URL,  # e.g https://www.google.com
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )


def record_and_paste():

    # click in start recording button
    # measure time of no change in text area
    #    after 2 secs of no change in text area, copy and paste
    #       copy text area (selenium Ctrl+c)
    #       paste text area (pyautogui Ctrl+v)
    #       delete text area (selenium Ctrl+a, delete)
    # stop recording

    # start recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    # wait to think about to what to say
    # sleep(2)

    # if no change in text area for x secs, copy and paste
    while not is_text_stable(interval=1.8):
        # copy_text_to_clipboard(d)
        paste_text()  # pyautogui in user clipboard
        delete_text()  # selenium in site's text area
        break

    # stop recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()


def is_text_stable(interval=1.5):

    while True:
        previous_length = get_text_len(d)
        time.sleep(interval)
        current_length = get_text_len(d)
        print(current_length ,' ' , previous_length)

        if current_length == previous_length:
            return False


def get_text_len(d):
    # return clipboard length
    copy_text_to_clipboard(d)
    return len(pyperclip.paste())


def copy_text_to_clipboard(d):
    # click in text area
    # control + a
    # control + c

    # select_all_text(d)  # control + a
    # actions = ActionChains(d)
    # actions.key_down(Keys.CONTROL).send_keys('c').perform()
    # actions.key_up(Keys.CONTROL).perform()

    ta = d.find_element(By.XPATH, XPATH_LIBRARY['text_area'])
    actions = ActionChains(d)
    actions.move_to_element(ta).key_down(Keys.CONTROL).send_keys('a').send_keys('c').perform()
    actions.key_up(Keys.CONTROL).perform()

    # ta = d.find_element(By.XPATH, XPATH_LIBRARY['text_area'])
    # ta.send_keys(Keys.CONTROL, 'c')


    print('copied ' + pyperclip.paste())


def paste_text():
    pyautogui.hotkey('ctrl', 'v')
    print('pasted' + pyperclip.paste())
    sleep(2)


def delete_text():
    select_all_text(d)
    actions = ActionChains(d)
    actions.send_keys(Keys.DELETE).perform()
    print('deleted')


def select_all_text(d):
    ta = d.find_element(By.XPATH, XPATH_LIBRARY['text_area'])
    ta.send_keys(Keys.CONTROL, 'a')

    # actions = ActionChains(d)
    # actions.key_down(Keys.CONTROL).send_keys('a').perform()
    # actions.key_up(Keys.CONTROL).release(ta).perform()
    # actions.send_keys_to_element(ta, actions.key_down(Keys.CONTROL), 'a').perform()

def close_driver(d):
    d.close()
    d.quit()

# d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()
# //div[@id="output_box"]
# d.find_element(By.XPATH, '//div[@id="output_box"]').click()
# d.find_element(By.XPATH, '//div[@id="output_box"]/textarea')
# actions.move_to_element(ta).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).key_up(Keys.CONTROL).perform()
# actions.move_to_element(ta).key_down(Keys.CONTROL).send_keys('c').perform()
# actions.send_keys(Keys.CONTROL, 'a').perform()
# d.find_element(By.XPATH,



def run():
    global d  # used to allow to assign variables in exec()
    d = create_driver()
    d.get(TARGET_URL)
    grant_permissions()  # microphone, geo location, camera

    # subprocess.Popen(["python", "main.py"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                  stderr=subprocess.PIPE)

    keyboard.add_hotkey('ctrl+shift+ñ', record_and_paste)  #args=('Hello from shortcut!',)

    # execution_wheel(d)

    while True:
        keyboard.wait('esc')
        # i = input("Enter additional data (or 'exit' to stop): ")
        # if i == 'q':
        #     break
        # if i == '':
        #     pyperclip.copy(t + i)
        #     pyperclip.paste()


if __name__ == '__main__':
    run()
