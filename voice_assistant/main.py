import datetime
import re
from utils.speech import speak, listen
from commands.fetch_ball import fetch_ball
from commands.send_email import send_email
from commands.get_weather import get_weather
from commands.get_news import get_news
from commands.teach_pronunciation import teach_pronunciation
from commands.tell_about_famous_person import tell_about_famous_person
from commands.detect_faces import detect_faces
from commands.tell_about_self import tell_about_self
from commands.play_music import play_music
from commands.tell_joke import tell_joke
from commands.love import love_response
from commands.girlfriend import  girlfriend_response

from commands.hate import hate_response
from commands.sing_rhyme import sing_nursery_rhyme_from_youtube
import spacy # type: ignore

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Paths to the YOLO config, weights, and class names files
config_path = './yolo/yolov4.cfg'
weights_path = './yolo/yolov4.weights'
labels_path = './yolo/coco.names'

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def process_command(command):
    doc = nlp(command)
    if "fetch the ball" in command:
        fetch_ball()
    elif any(token.lemma_ in ["send", "email", "compose"] for token in doc):
        send_email()
    elif any(token.lemma_ in ["weather", "temperature", "forecast"] for token in doc):
        get_weather()
    elif any(token.lemma_ in ["news", "headline", "current events"] for token in doc):
        get_news()
    elif any(token.lemma_ in ["pronunciation", "speak", "accent", "speech"] for token in doc):
        teach_pronunciation()
    elif any(token.lemma_ in ["rhyme"] for token in doc):
        sing_nursery_rhyme_from_youtube()
    elif any(token.lemma_ in [ "biography", "information", "details"] for token in doc):
        tell_about_famous_person()
    elif any(token.lemma_ in ["face", "detect", "recognition", "identify", "can", "see", "look" ] for token in doc):
        try:
            detect_faces(config_path, weights_path, labels_path)
        except Exception as e:
            speak(f"Error during face detection: {e}")
    elif any(token.lemma_ in ["who", "yourself", "introduce", "identity"] for token in doc):
        tell_about_self()
    elif any(token.lemma_ in ["music", "song", "play", "audio", "relax"] for token in doc):
        play_music()
    elif any(token.lemma_ in ["love"] for token in doc):
        love_response()
    elif any(token.lemma_ in ["hate"] for token in doc):
        hate_response()
    elif any(token.lemma_ in ["girlfriend"] for token in doc):
        girlfriend_response()

    elif any(token.lemma_ in ["joke", "funny", "laugh", "bore", "lonely"] for token in doc):
        tell_joke()
    else:
        speak("I'm sorry, Can you please repeat?")

if __name__ == "__main__":
    greet()
    speak("How can I assist you ?")
    
    while True:
        command = listen().strip().lower()
        if command == 'goodbye':
            speak("Goodbye, See you later!")
            # break
            continue
        process_command(command)

