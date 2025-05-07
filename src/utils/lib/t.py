import subprocess

def copy_to_clipboard(text):
    try:
        # Open a subprocess to call `wl-copy` and pass the text
        process = subprocess.Popen(
            ["wl-copy"],
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
copy_to_clipboard("Hello, Wayland clipboard!")
