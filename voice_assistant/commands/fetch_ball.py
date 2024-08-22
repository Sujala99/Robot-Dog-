# commands/fetch_ball.py

from utils.speech import speak
import time

def fetch_ball():
    speak("Fetching the ball...")
    time.sleep(2)
    speak("Woof! Here is your ball!")
