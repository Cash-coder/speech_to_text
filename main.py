from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from time import sleep
import pyperclip
import keyboard
import os  # to remove screenshot in testing mode
import pyautogui
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import subprocess
# import time


# service_args, to force headless

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
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    # from webdriver_manager.chrome import ChromeDriverManager

    # import undetected_chromedriver as uc
    # opts = uc.ChromeOptions()
    # opts.headless=True
    # opts.add_argument('--headless')
    # opts.add_argument('--disable-gpu')
    # driver = uc.Chrome(options=opts)

    # driver = uc.Chrome(headless=True, use_subprocess=False)
    # driver.maximize_window()

    # opts = webdriver.ChromeOptions()



    from selenium import webdriver
    # from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import ChromeOptions

    options = ChromeOptions()
    # enable headless mode in Selenium
    # options = Options()
    # options.headless = True


    options.add_argument('--headless')


    # options.add_argument("--headless=new")
    # options.add_argument("--headless=old")
    # options.add_argument("--headless=chrome")
    # options.add_argument("--window-size=1920,1080")

    options.add_argument("--disable-web-security")
    options.add_argument("--no-default-browser-check")
    # options.add_argument("--disable-webgl")
    options.add_argument('--no-sandbox')
    options.add_argument('--incognito')
    # options.add_argument('-–disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2
    })

    options.add_argument('--user-data-dir=C:\\Users\\smart\\AppData\\Local\\Google\\Chrome\\User Data\\Default.')
    options.add_argument('--use-fake-ui-for-media-stream')
    options.add_argument('--use-fake-device-for-media-stream')
    options.add_argument('--allow-file-access-from-files')

    # options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    path = r"C:\Users\smart\Downloads\chromedriver_win32\chromedriver.exe"

    # path = r"C:\Users\smart\Downloads\chromedriver_win32\chromedriver.exe"
    # driver = webdriver.Chrome(executable_path=path, chrome_options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    service = Service(executable_path=path)

    driver = webdriver.Chrome(
        options=options,
        service=service,
        # other properties...
    )

    # driver.maximize_window()
    driver.set_window_size(800, 1200)


    # service = Service (executable_path=ChromeDriverManager().install() )
    # return webdriver.Chrome(service=service, options=options)

    return driver

def create_driver_2():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    # from webdriver_manager.chrome import ChromeDriverManager

    # import undetected_chromedriver as uc
    # opts = uc.ChromeOptions()


    bin_path = r"C:\Users\smart\Downloads\c_109\chrome-win\chrome.exe"
    driv_path = r"C:\Users\smart\Downloads\w113\chrome-win\chrome.exe"

    options = Options()
    # options.headless = True
    # options.add_argument('--headless')
    # options.add_argument("--headless=new")

    options.binary_location = bin_path
    dService = Service(driv_path)

    driver = webdriver.Chrome(service=dService, options=options)

    return driver


#  undetectable driver
def create_driver_3():
    import undetected_chromedriver as uc

    options = uc.ChromeOptions()
    options.headless=True
    options.add_argument('--headless')
    # options.add_argument("--headless=new")
    # options.add_argument("--headless=old")
    # options.add_argument("--headless=chrome")
    options.add_argument("--window-size=500,600")

    options.add_argument("--disable-web-security")
    options.add_argument("--no-default-browser-check")
    # options.add_argument("--disable-webgl")
    options.add_argument('--no-sandbox')
    # options.add_argument('--incognito')
    # options.add_argument('-–disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2
    })

    driver = uc.Chrome(options=options)


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

def remove_screenshot():
    try:
        os.remove('screenshot.png')
    except:
        pass

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
    print('clicked record button')
    remove_screenshot()

    # actions = ActionChains(d)
    # button = d.find_element(By.XPATH, XPATH_LIBRARY['record_button'])
    # actions.move_to_element(button).send_keys(Keys.ENTER).perform()

    d.save_screenshot("screenshot.png")
    print('screenshot taken')
    text = get_text()


    paste_text(text)

    # stop recording
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()
    # d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).send_keys(Keys.RETURN)
    # button = d.find_element(By.XPATH, XPATH_LIBRARY['record_button'])
    # actions.move_to_element(button).send_keys(Keys.ENTER).perform()



def get_text():
    tm = d.find_element(By.XPATH, XPATH_LIBRARY['text_mirror'])
    wait_until_started_to_change(XPATH_LIBRARY['text_mirror'])
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


def wait_until_started_to_change(xpath_element):
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
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')


def close_driver(d):
    d.close()
    d.quit()


def run():
    global d  # used to allow to assign variables in exec()
    # d = create_driver()
    # d = create_driver_2()
    d = create_driver_3()

    d.get(TARGET_URL)
    grant_permissions()  # microphone, geo location, camera

    # subprocess.Popen(["python", "main.py"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                  stderr=subprocess.PIPE)

    keyboard.add_hotkey('ctrl+shift+ñ', record_and_paste)  #args=('Hello from shortcut!',)

    # only for testing
    # execution_wheel(d)

    while True:

        keyboard.wait('esc')  # trigger shortcut

        i = input("Trigger with shortcut Control + Shit + ñ or ('exit' to stop): ")
        if i == 'q':
            print('exiting ... ')
            break


if __name__ == '__main__':
    run()
