

import time
import logging
from utils.speech import speak, listen
import spacy
from textblob import TextBlob

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Set up logging
logging.basicConfig(filename='pronunciation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def teach_pronunciation():
    try:
        speak("Sure, please spell the word you would like me to pronounce.")
        spelled_word = listen().replace(' ', '')
        if spelled_word:
            word = ''.join(spelled_word.split())
            speak(f"Let's learn how to pronounce the word {word}.")
            speak("Listen carefully to the correct pronunciation.")
            speak(word)
            speak("Now, please try to repeat after me.")

            attempts_left = 3
            while attempts_left > 0:
                speak("Please say the word after the beep.")
                time.sleep(1)
                speak("Beep")

                attempt = listen()
                if attempt:
                    similarity_score = calculate_similarity(word, attempt)
                    logging.info(f"Attempt: {attempt}, Similarity Score: {similarity_score}")

                    if similarity_score >= 0.9:
                        speak("Excellent! You pronounced it perfectly!")
                        return
                    else:
                        feedback = get_feedback(word, attempt, similarity_score)
                        speak(feedback)
                        speak("Let's try again.")
                        attempts_left -= 1
                else:
                    speak("I didn't hear anything. Let's try again.")
                    attempts_left -= 1

            speak("You've used all your attempts. Let's move on.")
            speak(f"The correct pronunciation of {word} is: {word}")
        else:
            speak("I didn't catch that. Please try again.")
    except Exception as e:
        logging.error(f"Error in teach_pronunciation: {e}")
        speak("Sorry, there was an error in processing your request. Please try again later.")

def calculate_similarity(word1, word2):
    doc1 = nlp(word1)
    doc2 = nlp(word2)
    return doc1.similarity(doc2)

def get_feedback(correct_word, user_word, similarity_score):
    if similarity_score >= 0.8:
        return "Not bad, but let's try to improve a bit more."
    elif similarity_score >= 0.6:
        return f"You're getting there! Focus on the sound of the word '{correct_word}'."
    elif similarity_score >= 0.4:
        return f"It's close, but let's work on getting it right. Pay attention to the pronunciation of '{correct_word}'."
    else:
        return f"Hmm, it seems there's still some room for improvement. Try to pronounce '{correct_word}' more clearly."

# if __name__ == "__main__":
#     teach_pronunciation()
