import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the configured voice ID
engine.setProperty('rate', 220)    # Speed in words per minute
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
engine.setProperty('pitch', 1.1)   # Pitch of the voice (0.5 to 2.0)

recognizer = sr.Recognizer()






def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 400  # Increase this value to reduce sensitivity
        audio = recognizer.listen(source)

    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("User said:", query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        speak(f"Could not request results; {e}")
        return ""


