from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)
last_message = "" # Holds the most recent message
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
commands = {"ADD": 1,
            "UPDATE": 2,
            "DELETE": 3,
            "CLEAR": 4,
            "SHOW": 5}
birthdays = pd.read_excel("Birthdays.xlsx", sheet_name="Sheet1") # Used to update the excel sheet holding data

# clears all records
def clear():
    empty = pd.DataFrame(columns = birthdays.columns)
    with pd.ExcelWriter("Birthdays.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            empty.to_excel(writer, sheet_name="Sheet1",index=False)

# Adds a record to the database (of the name given)
def add(name, day, month):
    global birthdays
    new_data = {"Name" : name.lower(), 
                "Day" : day,
                "Month" : month.lower()}
    birthdays = pd.concat([birthdays, pd.DataFrame([new_data])], ignore_index=True)
    
# Updates an existing record in the database (if name exists)
def update(name, day, month):
    global birthdays
    if birthdays.empty:
        return 0
    column_name = "Name"
    mask = birthdays[column_name] == name.lower() # Holds records that satisfy conditions
    if mask.any():
        birthdays.loc[mask, ["Day" ,"Month"]] = [day, month]
        with pd.ExcelWriter("Birthdays.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            birthdays.to_excel(writer, sheet_name="Sheet1",index=False)
        return 1
    else:
        return 0

# Display details of the provided name
def show(name):
    global birthdays
    column_name = "Name"
    match = birthdays[birthdays[column_name] == name.lower()] # Holds records that satisfy conditions
    if birthdays.empty:
        return 0
    if match.empty:
        return 0
    else:
        return 1

# Deletes the record of the name provided
def delete(name):
    global birthdays
    if birthdays.empty:
        return 0
    column_name = "Name"
    mask = birthdays[column_name] == name.lower()
    if mask.any():
        birthdays = birthdays[birthdays["Name"] != name.lower()]
        with pd.ExcelWriter("Birthdays.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            birthdays.to_excel(writer, sheet_name="Sheet1",index=False)
        return 1
    else:
        return 0 
      
# Used to check if the input is in correct format, used to pick the message to return
"""STATUS CODES
    *************
    0 - Format or invalid error
    1 - successful clear 
    2 - unsuccesful clear
    3 - successful delete
    4 - unsuccessful delete
    5 - succesful add
    6 - succesful update
    7 - unsuccessful update
    8 - successful show
    9 - unsuccessful show
    11 - unsuccesful add

    ****************
"""
def processMessage(message:list):
    global birthdays
    if len(message) == 1:
        if message[0].upper() == "CLEAR":
            clear()
            return 1
        else:
            return 0
    elif len(message) == 2:
        if message[0].upper() == "DELETE":
            if(delete(message[1])):
                return 3
            else:
                return 4
        elif message[0].upper() == "SHOW":
            if(show(message[1])):
                return 8
            else:
                return 9
        else:
            return 0
    elif len(message) == 4:
        try:
            day = int(message[2])
        except:
            return 0
        month = message[-1]
        if ((day < 1 or day > 32) or (month.lower() not in months)):
            return 11
        if message[0].upper() == "ADD":
            add(message[1], day, month)
            return 5
        elif message[0].upper() == "UPDATE":
            if(update(message[1], day, month)):
                return 6
            else:
                return 7
        else:
            return 0
    else:
        return 0

# Used to send reply to display status
@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp_reply():
    global last_message
    global birthdays

    incoming_msg = request.form.get("Body")  #input message    
    sender = request.form.get("From")           
    last_message = incoming_msg     # recent message

    message_info = last_message.split(" ")  # split the input into different categories
    signal = processMessage(message_info)   # Recieve status code
    text = ""
    match signal:
        case 0:
            text = (
"Format error or invalid. Please provide a valid input and follow the format:\n"
"<command> <Name> <Birth_day> <Birth_month>\n"
"1.Valid Commands: ADD, UPDATE, DELETE, SHOW, CLEAR\n"
"2.The full name SHOULD be seperated by underscores.\n"
"3.Provide the full month name.\n"
"4.Read documentation for all the information.\n"
)
        case 1:
            text = f"All data has been cleared successfully. Your records are cleared."
        case 3:
            text = f"{message_info[1]}'s record has been deleted successfully."
        case 4:
            text = f"Deletion unsuccessful. The name was not found."
        case 5:
            text = f"Successfully added {message_info[1]}'s birthday on {message_info[2]} {message_info[3]}."
        case 6:
            text = f"Successfully updated {message_info[1]}'s birthday to {message_info[2]} {message_info[3]}."
        case 7:
            text = f"Update unsuccesful. The name was not found."
        case 8:
            text = ""
            for row in birthdays.itertuples(index=True):
                if row.Name == message_info[1].lower():
                    text += f"{row.Name}'s birthday is on {row.Day} {row.Month}\n"
        case 9:
            text = f"Could not find any records with the given name."
        case 11:
            text = f"Please provide a valid date and month."
        case _:
            text = f"Something went wrong. Try again."

    response = MessagingResponse()
    response.message(text)
    return str(response)

if __name__ == "__main__":
    app.run(port=8080)