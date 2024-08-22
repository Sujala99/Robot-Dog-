# # commands/tell_joke.py

# from utils.speech import speak
# import random
# import requests
# from config import joke_url

# # Function to tell a joke
# def tell_joke():
#     url = joke_url

#     try:
#         response = requests.get(url)
#         joke_data = response.json()
#         joke = joke_data['setup'] + " " + joke_data['punchline']
#         speak("Here's a joke for you.")
#         speak(joke)
#     except Exception as e:
#         print(e)
#         speak("Sorry, I couldn't fetch a joke at the moment.")


import requests
import random
import logging
from utils.speech import speak
from config import joke_url

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fallback jokes
fallback_jokes = [
    {"setup": "Why don't scientists trust atoms?", "punchline": "Because they make up everything!"},
    {"setup": "What do you get if you cross a cat with a dark horse?", "punchline": "Kitty Perry"},
    {"setup": "Why was the math book sad?", "punchline": "Because it had too many problems."}
]

# Function to fetch a joke from the API
def fetch_joke_from_api(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    joke_data = response.json()
    return joke_data

# Function to get a joke
def get_joke():
    try:
        joke_data = fetch_joke_from_api(joke_url)
        joke = f"{joke_data['setup']} {joke_data['punchline']}"
        logging.info("Joke fetched from API successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        joke_data = random.choice(fallback_jokes)
        joke = f"{joke_data['setup']} {joke_data['punchline']}"
        logging.info("Using fallback joke.")
    except KeyError as e:
        logging.error(f"Key error: {e}")
        joke_data = random.choice(fallback_jokes)
        joke = f"{joke_data['setup']} {joke_data['punchline']}"
        logging.info("Using fallback joke.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        joke_data = random.choice(fallback_jokes)
        joke = f"{joke_data['setup']} {joke_data['punchline']}"
        logging.info("Using fallback joke.")
    
    return joke

# Function to tell a joke
def tell_joke():
    joke = get_joke()
    speak("Haha... Let's laugh!")
    speak(joke)

# Example usage
if __name__ == "__main__":
    tell_joke()

