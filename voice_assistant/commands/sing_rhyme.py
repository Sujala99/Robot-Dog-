import youtube_dl
import os
from utils.speech import speak

def search_youtube(query):
    # Simulate search results; replace with actual YouTube search API integration if needed
    return ["yCjJyiqpAuU"]  # Example video ID for "Twinkle Twinkle Little Star"

def sing_nursery_rhyme_from_youtube():
    speak("Let's sing a nursery rhyme together.")
    query = "twinkle twinkle little star"  # Example query for "Twinkle Twinkle Little Star"
    video_ids = search_youtube(query)
    
    if video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        
        # Define options for youtube_dl
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'rhyme.mp3',
            'verbose': True
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        os.system('start rhyme.mp3')
        speak("Now singing Twinkle Twinkle Little Star!")
    else:
        speak("Sorry, I couldn't find a nursery rhyme video.")


    
