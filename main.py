# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "a9a6f6bff6434fab84e02039c1612bb8"
transcriber = aai.Transcriber()

# transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
transcript = transcriber.transcribe(r"C:\Users\smart\OneDrive\Documentos\Grabaciones de sonido\Grabación.m4a")

print(transcript.text)
