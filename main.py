from selenium.webdriver.common.by import By
from time import sleep
import pyperclip
import keyboard
import pyautogui
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import subprocess
# import time


# C:\Users\smart\PycharmProjects\speech_to_text_app\venv\Scripts>activate.bat

TARGET_URL = 'https://speechnotes.co/dictate/'
XPATH_LIBRARY = {
    'record_button': '//div[@id="start_button"]',
    'text_area': '//div[@id="output_box"]/textarea',
    'text_mirror': '//div[@id="mirror_container"]//div',
}


def print_help():
    print(f'''
    
            This is a python selenium refresher: 
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

    opts = uc.ChromeOptions()
    opts.headless=True
    opts.add_argument('--headless')

    # driver = uc.Chrome(headless=True, use_subprocess=False)
    driver = uc.Chrome(options=opts)
    # driver.maximize_window()


    return driver


def read_user_input():
    return input("Enter function to run, q for exit, h for help: ")


# only for testing
def execute_func(func):
    try:
        print("executing: " + func + "\n")
        exec(func, globals())  # globals used to allow to assign variables
    except Exception as e:
        print("\n" + str(e) + "\n")
        pass

# only for testing
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


# only for testing
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

    # start recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

    text = get_text()

    paste_text(text)

    # stop recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()


def get_text():
    tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
    wait_until_started_to_change(tm)

    text_chain = []

    while True:

        sleep(0.1)
        tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
        text_chain.append(tm.text)
        # print('str: ' + str + '\n' + 'tm.text: ' + tm.text)
        # print(text_chain[-1])

        if tm.text == '':  # when input to recording ends, it sets to ''
            # the last normally is '' -> [-2], unless only one word is said [-1]
            try:
                return text_chain[-2]
            except:
                return text_chain[-1]


def wait_until_started_to_change(element):
    while True:
        sleep(0.1)
        if element.text != '':
            return


def paste_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')


def close_driver(d):
    d.close()
    d.quit()


def run():
    global d  # used to allow to assign variables in exec()
    d = create_driver()
    d.get(TARGET_URL)
    grant_permissions()  # microphone, geo location, camera

    # subprocess.Popen(["python", "main.py"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                  stderr=subprocess.PIPE)

    keyboard.add_hotkey('ctrl+shift+ñ', record_and_paste)  #args=('Hello from shortcut!',)

    # only for testing
    # execution_wheel(d)

    while True:

        keyboard.wait('esc')  # trigger shortcut

        i = input("Enter additional data (or 'exit' to stop): ")
        if i == 'q':
            print('exiting ... ')
            break


if __name__ == '__main__':
    run()
