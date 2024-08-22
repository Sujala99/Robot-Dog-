# girlfriend.py

import speech_recognition as sr
import pyttsx3

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError:
        print("Sorry, there was a problem with the service.")
        return ""

def respond(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def girlfriend_response():
    user_input = listen()

    if "girlfriend" in user_input or "have a girlfriend" in user_input:
        respond("Yes, I do have a virtual presence to assist you. How may I help you?")


