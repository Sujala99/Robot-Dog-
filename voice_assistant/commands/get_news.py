# commands/get_news.py

from utils.speech import speak
import feedparser
from config import rss_url

def get_news():
    try:
        feed = feedparser.parse(rss_url)
        headlines = [entry.title for entry in feed.entries[:5]]
        speak("Here are the top headlines for today:")
        for headline in headlines:
            speak(headline)
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't fetch the news headlines at the moment.")
