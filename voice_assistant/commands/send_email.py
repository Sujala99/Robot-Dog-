# # commands/send_email.py

# from utils.speech import speak, listen
# import yagmail
# from config import sender_email

# def send_email():
#     speak("Whom should I send the email to?")
#     receiver_email = listen()
#     speak("What should be the subject of the email?")
#     subject = listen()
#     speak("What should I write in the body of the email?")
#     body = listen()
    
#     yag = yagmail.SMTP(sender_email)
    
#     try:
#         yag.send(
#             to=receiver_email,
#             subject=subject,
#             contents=body,
#         )
#         speak("Email has been sent successfully.")
#     except Exception as e:
#         print(e)
#         speak("Sorry, I couldn't send the email.")



# commands/send_email.py

from utils.speech import speak, listen
import yagmail
import re
from config import sender_email

def validate_email(email):
    """Validate the email address using a regex pattern."""
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email) is not None

def send_email():
    speak("Whom should I send the email to?")
    while True:
        receiver_email = listen()
        if validate_email(receiver_email):
            break
        else:
            speak("The email address seems invalid. Please provide a valid email address.")

    speak("What should be the subject of the email?")
    subject = listen()

    speak("What should I write in the body of the email?")
    body = listen()

    speak("Please confirm, should I send the email now? Say 'yes' to send or 'no' to cancel.")
    confirmation = listen().lower()

    if confirmation in ['yes', 'yeah', 'yup', 'send']:
        yag = yagmail.SMTP(sender_email)

        try:
            yag.send(
                to=receiver_email,
                subject=subject,
                contents=body,
            )
            speak("Email has been sent successfully.")
            # Log the sent email details
            with open('email_log.txt', 'a') as log_file:
                log_file.write(f"To: {receiver_email}\nSubject: {subject}\nBody: {body}\n\n")
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't send the email.")
    else:
        speak("Email sending has been cancelled.")

