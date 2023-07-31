import requests
from githubConnector import get_streak, has_contributed_today
from api_keys import PUSHOVER_API_KEY, PUSHOVER_USER_KEY

def notify_phone(message, user = "u1ebamr9d7nzquhxkqvcxfho8wtzgh"):
    r = requests.post("https://api.pushover.net/1/messages.json", data = {
            "token": PUSHOVER_API_KEY,
            "user": PUSHOVER_USER_KEY,
            "message": message
        },
        files = {
            "attachment": ("image.jpg", open("logo.jpeg", "rb"), "image/jpeg")
        }
    )

def morning_message():
    if has_contributed_today():
        notify_phone(f"Wow, you are an early bird! Your streak is now {get_streak() + 1} days.")
    else:
        notify_phone(f"Wakey, wakey, time to hack! Your streak is {get_streak()} days.")

def afternoon_message():
    if has_contributed_today():
        notify_phone(f"Keep up the good work! Your streak is now {get_streak() + 1} days.")
    else:
        notify_phone(f"Time is running out! Don't lose your streak of {get_streak()} days.")

def evening_message():
    if has_contributed_today():
        notify_phone(f"Take a well earned rest! Your streak is now {get_streak() + 1} days.")
    else:
        notify_phone(f"This is your last chance to save your streak of {get_streak()} days.")


morning_message()
afternoon_message()
evening_message()