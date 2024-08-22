# love.py

import speech_recognition as sr
import pyttsx3
import requests

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

def get_quote(topic):
    url = f"https://api.quotable.io/quotes?tags={topic}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['content']
    return None

def love_response():
    user_input = listen()

    if "i love" in user_input:
        # Extract what the user loves
        love_topic = user_input.split("i love ", 1)[1]
        
        # Get a quote related to the love topic
        quote = get_quote(love_topic)

        if quote:
            respond(f"That's wonderful! You love {love_topic}. Here's a quote for you: {quote}")
        else:
            respond(f"That's wonderful! You love {love_topic}.")


