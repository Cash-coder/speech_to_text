from utils.lib.driver import create_driver, create_normal_driver, grant_permissions
from utils.config import TARGET_URLS, XPATH_LIBRARY, VOICE_COMMANDS
from utils.lib.text import get_text, paste_text, paste_text_2, paste_text_3
from selenium.webdriver.common.by import By
from time import sleep
import logging
from selenium.webdriver.support.ui import Select

# HEADLESS = False
HEADLESS = True
is_paused = False


logging.basicConfig(filename='../logs.log', level=logging.DEBUG)

def press_record_btn(d):
    sleep(2)
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()

def check_voice_command(text: str) -> bool | str:
    """Check if text contains any command and
      return the command code if found, return False otherwise"""

    for command_phrase, command_code in VOICE_COMMANDS.items():
        if command_phrase.lower() in text.lower():
            return command_code
    # return false if no command found
    return False

def execute_command(d, command_code: str) -> None:
    """match command code with execution code and execute code"""
    import subprocess
    global is_paused

    if command_code == 'toggle_record':
        # is_paused = True
        is_paused = not is_paused # toggle pause from true to false and viceversa
        print("command pause")
        print("is_paused is :", is_paused, "\n")
        subprocess.run(["notify-send", "STT recording toggle"])
        # press_record_btn(d)

    elif command_code == 'ES':
        print("switching to Spanish")
        
        d.find_element(By.XPATH, XPATH_LIBRARY['lan_selector']).click()
        sleep(1)
        d.find_element(By.XPATH, XPATH_LIBRARY['ES']).click()
        sleep(1)
        press_record_btn(d)
        
        subprocess.run(["notify-send", "Cambiando a Español | Bienvenido =)"])

    elif command_code == 'EN':
        print("switching to English")
        
        d.find_element(By.XPATH, XPATH_LIBRARY['lan_selector']).click()
        sleep(1)
        d.find_element(By.XPATH, XPATH_LIBRARY['EN']).click()
        sleep(1)
        press_record_btn(d)
        
        subprocess.run(["notify-send", "Cambiando a Inglés | Bienvenido =)"])

def run():

    d = create_normal_driver(headless=HEADLESS)   
    d.get(TARGET_URLS['dictation_url'])

    grant_permissions(d)  # microphone, geo location, camera

    # open second tab to get grammar improvement suggestions
    # open_second_tab(d, TARGET_URLS['grammar_url']) # open grammar tab
    # switch_to_american_english(d)

    execute_command(d, "EN")
    # press_record_btn(d)
    print('\nProgram running!\n')
    print("These are the voice commands:")
    for command, action in VOICE_COMMANDS.items():
        print(f" - '{command}' → {action}")

    while True:
        # get text from STT app UI
        text = get_text(d)

        # check if voice command is present in text
        command_code = check_voice_command(text)
        if command_code:
            execute_command(d, command_code)
            # avoid pasting command code as text
            continue

        if is_paused is False:
            paste_text_3(text)

if __name__ == '__main__':
    run()
