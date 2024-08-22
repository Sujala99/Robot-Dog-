# commands/tell_about_famous_person.py

from utils.speech import speak, listen
import wikipedia
import re

def tell_about_famous_person():
    speak("Whom would you like to know about?")
    person = listen()
    if person:
        try:
            speak(f"Searching information about {person}...")

            # Use Wikipedia API to fetch search results
            search_results = wikipedia.search(person)
            if not search_results:
                speak(f"Sorry, I couldn't find any information about {person}.")
                return

            # Take the top result
            page_title = search_results[0]
            page = wikipedia.page(page_title)

            # Fetch summary, birth date, and notable works if available
            summary = wikipedia.summary(page_title, sentences=3)

            # Attempt to extract birth date and other info from the page content
            page_content = page.content
            birth_date = extract_birth_date(page_content)
            notable_works = extract_notable_works(page_content)

            speak(f"{summary}")

            if birth_date:
                speak(f"{person} was born on {birth_date}.")

            if notable_works:
                speak(f"Some notable works of {person} include {', '.join(notable_works[:3])}.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"There are multiple results for {person}. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak(f"Sorry, I couldn't find any information about {person}.")
        except Exception as e:
            speak("Sorry, I couldn't fetch the information at the moment.")
            print(e)

def extract_birth_date(content):
    birth_date_pattern = r'\b(?:born|Born)\s+(?:on\s+)?(\w+\s+\d{1,2},\s+\d{4})\b'
    match = re.search(birth_date_pattern, content)
    if match:
        return match.group(1)
    return None

def extract_notable_works(content):
    lines = content.split('\n')
    notable_works = []
    for line in lines:
        if 'notable work' in line.lower():
            notable_works.append(line)
    return notable_works
