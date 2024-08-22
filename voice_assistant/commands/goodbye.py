# goodbye.py
from utils.speech import speak
import voice_assistant.global_state as global_state

def say_goodbye():
    global_state.is_active = False
    speak("Goodbye! I will stop listening until you say 'hey X'.")
