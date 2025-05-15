from selenium.webdriver.common.by import By
from ..config import XPATH_LIBRARY
from time import sleep
import logging
import pyperclip
import subprocess



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
    # old_clipboard = pyperclip.paste()

    # copy text to clipboard
    pyperclip.copy(text)
    
    # paste for windows
    # pyautogui.hotkey('ctrl', 'v')

    # paste text,for linux hyprland
    subprocess.run(["wtype", text])

    # copy into the clipboard the previous content
    # pyperclip.copy(old_clipboard)

def paste_text_3(text):
    subprocess.run(["wtype", text])  

    #process = subprocess.run(
        #['echo', f'{text}', '|', 'wl-copy']
        #['wl-copy'],
        #input=text.encode('utf-8'),  # Pass text to stdin
        #stdin=subprocess.PIPE,
        # stdout=subprocess.PIPE, 
        # stderr=subprocess.PIPE,
        # check=True
    #)

    # if activated it creates a bug w primary selection sync
    # is this is to log the result in the clipoard history ?
    # process = subprocess.Popen(
    # ['wl-copy'], 
    # stdin=subprocess.PIPE,  # Pass input via stdin
    # stdout=subprocess.PIPE, 
    # stderr=subprocess.PIPE
    # )
    
    #process.kill()



def paste_text_2(text):
    try:
        # Open a subprocess to call `wl-copy` and pass the text
        process = subprocess.Popen(
            ["wl-paste", "-p"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate(input=text.encode("utf-8"))
        # Ensure the process exits without issues
        if process.returncode != 0:
            raise RuntimeError(f"wl-copy failed with error: {process.stderr.read().decode('utf-8')}")
        print("Text copied to clipboard successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
#copy_to_clipboard("Hello, Wayland clipboard!")

