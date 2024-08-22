# # commands/get_weather.py

# from utils.speech import speak, listen
# import pyowm
# from config import owm_api_key

# def get_weather():
#     speak("Which city's weather would you like to know?")
#     city = listen()
#     owm = pyowm.OWM(owm_api_key)

#     try:
#         observation = owm.weather_manager().weather_at_place(city)
#         weather = observation.weather
#         temperature = weather.temperature('celsius')['temp']
#         status = weather.detailed_status
#         speak(f"The current temperature in {city} is {temperature} degrees Celsius with {status}.")
#     except Exception as e:
#         print(e)
#         speak("Sorry, I couldn't fetch the weather information at the moment.")




# commands/get_weather.py

# from utils.speech import speak, listen
# import pyowm
# from config import owm_api_key

# def get_weather():
#     speak("Which city's weather would you like to know?")
#     city = listen()

#     if not city:
#         speak("Sorry, I didn't catch that. Could you please repeat the city name?")
#         city = listen()

#     owm = pyowm.OWM(owm_api_key)

#     try:
#         # Search for the city and get the weather observation
#         observation = owm.weather_manager().weather_at_place(city)
#         weather = observation.weather

#         # Extract weather details
#         temperature = weather.temperature('celsius')['temp']
#         status = weather.detailed_status
#         humidity = weather.humidity
#         wind_speed = weather.wind()['speed']
#         sunrise_time = weather.sunrise_time(timeformat='iso')
#         sunset_time = weather.sunset_time(timeformat='iso')

#         # Construct the response
#         response = (
#             f"The current weather in {city} is {status}. "
#             f"The temperature is {temperature} degrees Celsius. "
#             f"The humidity is {humidity}% and wind speed is {wind_speed} m/s. "
#             f"The sun rises at {sunrise_time} and sets at {sunset_time}."
#         )

#         speak(response)

#     except pyowm.exceptions.NotFoundError:
#         speak(f"Sorry, I couldn't find weather information for {city}. Please try another city.")
#     except pyowm.exceptions.APIRequestError:
#         speak("There was an issue connecting to the weather service. Please try again later.")
#     except Exception as e:
#         speak("Sorry, there was a problem fetching the weather information.")
#         print(e)




# commands/get_weather.py

from utils.speech import speak, listen
import pyowm
from config import owm_api_key

def get_weather():
    speak("Which city's weather would you like to know?")
    city = listen()

    if not city:
        speak("Sorry, I didn't catch that. Could you please repeat the city name?")
        city = listen()

    owm = pyowm.OWM(owm_api_key)

    try:
        observation = owm.weather_manager().weather_at_place(city)
        weather = observation.weather

        # Get weather details
        temperature = weather.temperature('celsius')['temp']
        status = weather.detailed_status
        humidity = weather.humidity
        wind_speed = weather.wind()['speed']
        sunrise_time = weather.sunrise_time(timeformat='iso').split('T')[1][:5]
        sunset_time = weather.sunset_time(timeformat='iso').split('T')[1][:5]

        # Construct the response
        response = (
            f"The current weather in {city} is {status.lower()}. "
            f"The temperature is {temperature} degrees Celsius. "
            f"The humidity is {humidity}% and the wind speed is {wind_speed} meters per second. "
            f"The sun will rise at {sunrise_time} and set at {sunset_time}."
        )

        speak(response)

    except pyowm.exceptions.NotFoundError:
        speak(f"Sorry, I couldn't find weather information for {city}. Please try another city.")
    except pyowm.exceptions.APIRequestError:
        speak("There was an issue connecting to the weather service. Please try again later.")
    except Exception as e:
        speak("Sorry, there was a problem fetching the weather information.")
        print(e)

