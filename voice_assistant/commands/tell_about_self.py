# # commands/tell_about_self.py

# from utils.speech import speak

# def tell_about_self():
#     speak("I am X, your voice assistant. I can help you with various tasks like fetching the ball, sending emails, getting weather updates, news, and much more.")




# commands/tell_about_self.py

from utils.speech import speak, listen
import datetime

def tell_about_self():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    intro = ("Hello! I am X, your voice assistant. "
             "I can help you with a variety of tasks such as fetching the weather, sending emails, "
             "getting the latest news updates, performing Wikipedia searches, setting reminders, "
             "and even providing some entertainment with jokes or trivia. It's currently "
             f"{current_time}.")
    
    speak(intro)
    
    speak("Would you like to hear about a specific feature? Please say 'yes' or 'no'.")
    response = listen().lower()
    
    if response in ['yes', 'yeah', 'yup']:
        speak("Great! Here are some features you can ask about: Weather, Emails, News, Wikipedia, Reminders, Jokes, Trivia. "
              "Which one would you like to know more about?")
        feature = listen().lower()
        
        if 'weather' in feature:
            speak("With the weather feature, you can ask me for the current weather or a forecast for any city. "
                  "I can provide you with temperature, humidity, wind speed, and weather conditions.")
        elif 'emails' in feature:
            speak("Using the email feature, I can help you compose and send emails. "
                  "You can dictate the recipient, subject, and body of the email.")
        elif 'news' in feature:
            speak("With the news feature, I can provide you with the latest headlines and updates from various categories such as technology, sports, and entertainment.")
        elif 'wikipedia' in feature:
            speak("The Wikipedia feature allows you to ask me about any topic, and I will fetch a summary from Wikipedia for you.")
        elif 'reminders' in feature:
            speak("I can help you set reminders for your tasks and events. Just tell me what you need to be reminded about and when.")
        elif 'jokes' in feature:
            speak("I can tell you a variety of jokes to lighten the mood. Just ask me to tell you a joke.")
        elif 'trivia' in feature:
            speak("With the trivia feature, I can provide you with interesting facts and trivia on various topics. Just ask me to tell you some trivia.")
        else:
            speak("I didn't recognize that feature. Please try again later.")
    else:
        speak("Alright! If you need any help, just ask me about any of my features.")

# Usage example
if __name__ == "__main__":
    tell_about_self()

