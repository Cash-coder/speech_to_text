import subprocess


def get_text():

    # get the latest entry from clipboard history
    result = subprocess.run(
        ["bash", "-c", "cliphist list | head -n 1 | cut -f2"],
        #input=text.encode('utf-8'),
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip() 


def paste_text(text): 

    # force control+v to paste
    subprocess.run(["wtype", "-M", "ctrl", "-M", "shift", "-k", "v", "-m", "shift", "-m", "ctrl"])

    # this process sync primary selection with clipboard
    # it conflicts with the wl-copy process from TTS program (text to speech)
    # kill it and create a new one that won't conflict with TTS
    subprocess.run(
        ["pkill", "-f", "wl-paste -p -w wl-copy"]
    )

    #leave running a fresh process of wl-paste
    subprocess.run(
        ["wl-paste", "-p", "-w", "wl-copy"]
        # stdin=subprocess.PIPE,
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
    )


if __name__ == '__main__':
    paste_text( 
                get_text()
    ) 

