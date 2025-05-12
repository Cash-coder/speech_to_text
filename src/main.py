from utils.lib.driver import create_driver, create_normal_driver, grant_permissions
from utils.config import TARGET_URLS, XPATH_LIBRARY
from utils.lib.text import get_text, paste_text, paste_text_2, paste_text_3
from selenium.webdriver.common.by import By
from time import sleep
import logging

# HEADLESS = False
HEADLESS = True

VOICE_COMMANDS = {
    "stop execution": "pause",    
    "start execution": "start",    
    "switch to spanish": "ES",    
    # "",    
}

logging.basicConfig(filename='../logs.log', level=logging.DEBUG)

def press_record_btn(d):
    sleep(2)
    d.find_element(By.XPATH, XPATH_LIBRARY['record_button']).click()
    print('\nProgram running\n')

def check_voice_command(text: str) -> bool | str:
    """Check if text contains any command and
      return the command code if found, return False otherwise"""

    for command_phrase, command_code in VOICE_COMMANDS.items():
        if command_phrase.lower() in text.lower():
            return command_code
    # return false if no command found
    return False

def execute_command(command_code: str, d) -> None:
    """match command code with execution code and execute code"""
    import subprocess

    if command_code == 'pause':
        print("command pause")
        subprocess.run(["notify-send", "STT Execution Paused"])
        press_record_btn(d)

    elif command_code == "start":
        print("Started TTS execution")
        subprocess.run(["notify-send", "STT Execution Started"])
        press_record_btn(d)

    elif command_code == 'ES':
        print("switching to Spanish")
        subprocess.run(["notify-send", "Cambiando a Español", "Bienvenido =)"])


def run():

    d = create_normal_driver(headless=HEADLESS)   
    d.get(TARGET_URLS['dictation_url'])

    grant_permissions(d)  # microphone, geo location, camera

    # open second tab to get grammar improvement suggestions
    # open_second_tab(d, TARGET_URLS['grammar_url']) # open grammar tab
    # switch_to_american_english(d)

    press_record_btn(d)

    while True:
        # get text from STT app UI
        text = get_text(d)

        # check if voice command is present in text
        command_code = check_voice_command(text)
        if command_code:
            execute_command(command_code, d)
            # avoid pasting command code as text
            continue


        paste_text_3(text)


if __name__ == '__main__':
    run()
