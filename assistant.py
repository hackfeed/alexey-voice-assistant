import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime


options = {
    "alias": ("alexey", "alex", "lyosha", "lesha", "leha", "lyoha",
              "leshidze"),
    "to_be_removed": ("say", "tell", "show", "what", "how"),
    "commands": {
        "current_time": ("current time", "time is it")
    }
}


def speak(phrase_to_speak):
    print(phrase_to_speak)
    speak_engine.say(phrase_to_speak)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="en-EN").lower()
        print("[log] Recognized: " + voice)

        if voice.startswith(options["alias"]):
            command = voice

            for option in options["alias"]:
                command = command.replace(option, "").strip()

            for option in options["to_be_removed"]:
                command = command.replace(option, "").strip()

            # распознаем и выполняем команду
            command = recognize_command(command)
            execute_command(command["command"])

    except sr.UnknownValueError:
        print("[log] Voice isn't recognized!")
    except sr.RequestError:
        print("[log] Unexpected error, check your connection!")


def recognize_command(command):
    RC = {"command": "", "percent": 0}
    for cmd, value in options['commands'].items():
        for option in value:
            vrt = fuzz.ratio(command, option)
            if vrt > RC["percent"]:
                RC["command"] = cmd
                RC["percent"] = vrt

    return RC


def execute_command(command):
    if command == "current_time":
        now = datetime.datetime.now()
        speak("Now is " + str(now.hour) + ":" + str(now.minute))

    else:
        speak("I don't know this command, could you repeate?")


recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=5)

with microphone as source:
    recognizer.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

speak("Welcome, I am Alexey, how can I help you?")

stop_listening = recognizer.listen_in_background(microphone, callback)
while True:
    time.sleep(0.1)  # infinity loop
