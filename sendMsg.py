import os
from twilio.rest import Client
import pandas as pd
from datetime import datetime

# Importing records
path = None
sheet = None
birthdays = pd.read_excel(f"{path}", sheet_name=f"{sheet}")

# Get today's date to check if there is a birthday today
date_today = datetime.now()
today = (date_today.month, date_today.day)

# Your account detail to be added here
# Get your account sid and authentication token after creating a twilio account
account_sid = None
auth_token = None

# add whatsapp numbers in the format: 'whatsapp:+<number>'
client = Client(account_sid, auth_token)
from_whatsapp = None
to_whatsapp = None

# Twilio sandbox resets every 2 days.
# Send your sandbox activation code every 24 hours to keep program running automatically
# body consists of your activation code reminder
client.messages.create(from_=from_whatsapp,
                       body='join rose-written',
                       to=to_whatsapp)

# Check for birthdays on current date
text = ""
for row in birthdays.itertuples(index=True, name="Row"):
    if row.Day == today[1] and row.Month == today[0]:
        text += f"Today is {row.Name}'s birthday!\n"

# If there is/are birthdays, get a reminder on WhatsApp
if text:
    client.messages.create(from_=from_whatsapp,
                       body=text,
                       to=to_whatsapp)