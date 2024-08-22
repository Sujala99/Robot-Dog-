# commands/play_music.py

from utils.speech import speak, listen
import os
import time
import pygame

# Update with your specific music file path
music_file = r"C:\Users\Acer\Downloads\Color_Out_-_Host.mp3"

def play_music():
    speak("Sure, playing music for you.")
    
    if os.path.exists(music_file):
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

        # Wait for music to start playing
        time.sleep(1)

        # Get start time
        start_time = time.time()

        while pygame.mixer.music.get_busy():
            # Check if 15 seconds have passed or user said "stop"
            if time.time() - start_time > 15 or listen() == "stop":
                pygame.mixer.music.stop()
                break

        speak("Music stopped.")
    else:
        speak("Sorry, I couldn't find the music file.")


