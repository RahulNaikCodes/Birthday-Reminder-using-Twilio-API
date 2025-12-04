import os
from twilio.rest import Client
import pandas as pd
from datetime import datetime

# Importing records
birthdays = pd.read_excel("Birthdays.xlsx", sheet_name="Sheet1")

# Get today's date to check if there is a birthday today
date_today = datetime.now()
today = (date_today.month, date_today.day)

# Your account detail to be added here 
# Get your account sid and authentication token after creating a twilio account
account_sid = 'ACe3204d114eb8da761e205b4fcd501f40'
auth_token = '2f06b2cffc50fffd266f62b8bc41f6ed'

# add whatsapp numbers in the format: 'whatsapp:+<number>'
client = Client(account_sid, auth_token)
from_whatsapp = 'whatsapp:+14155238886'
to_whatsapp = 'whatsapp:+919590525889'

# Twilio sandbox resets every 2 days.
# Send your sandbox activation code every 24 hours to keep program running automatically
# body consists of your activation code
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
    

