from ..config import TARGET_URLS
import logging

# set logger
logging.basicConfig(filename='logs.log', level=logging.INFO)


def create_normal_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless=new')
    # opts.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)  #, options=chrome_options)
    return driver


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


# microphone, geo location, camera
def grant_permissions(d):
    d.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": TARGET_URLS['dictation_url'],
            "permissions": ["geolocation", "audioCapture", "displayCapture", "videoCapture",
                            "videoCapturePanTiltZoom"]
        },
    )


def close_driver(d):
    d.close()
    d.quit()


