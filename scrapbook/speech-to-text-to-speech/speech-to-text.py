"""

Idea:
experiment with speech recognition, taking audio from microphone, and outputting as text.

sources/documentation:
https://realpython.com/python-speech-recognition/
    install pyaudio using https://stackoverflow.com/a/60666220
        >sudo apt-get install portaudio19-dev python3-pyaudio
        >pip install PyAudio

"""

import speech_recognition as sr

filename = "scrapbook/speech-to-text-to-speech/sample.wav"

r = sr.Recognizer()
data = sr.AudioFile(filename)
with data as source:
    audio = r.record(source)

print(r.recognize_google(audio))