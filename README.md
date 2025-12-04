# Birthday Reminder on WhatsApp using Twilio API

A **Flask-based Python application** that stores birthdays, manages records through WhatsApp commands, and automatically sends WhatsApp birthday messages using the **Twilio Sandbox**. The project can be hosted on **PythonAnywhere** to keep it running continuously.

---
## Features
- **Add a record** — `ADD <name> <day> <month>`
- **Update a record** — `UPDATE <name> <day> <month>`
- **Delete a record** — `DELETE <name>`
- **Retrieve a record** — `SHOW <name>`
- **Clear all records** — `CLEAR`

> **Note:** If using a full name, use **underscores** instead of spaces (e.g., `John_Doe`).

---
## Requirements
- Twilio account
- Account SID & Auth Token
- Twilio WhatsApp Sandbox number
- PythonAnywhere account for hosting
- Python installed locally

---
## User Guide & Notes
1. The Twilio WhatsApp Sandbox **deactivates every 48 hours**. You will receive a reminder to manually activate it — this cannot be automated.
2. Free Twilio accounts are limited to **50 WhatsApp messages per day**.
3. **Day** should be numeric (e.g., `23` not `23rd`).
4. **Month** must be spelled fully (e.g., `January`, not `Jan`).

---
## Installation & Setup
### 1. Twilio Setup
1. Create a [Twilio account](https://twilio.com/login).
2. Set up your **WhatsApp Sandbox** and obtain:
   - `ACCOUNT_SID`
   - `AUTH_TOKEN`
   - Twilio sandbox WhatsApp number

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Local Testing (Optional)
You need **ngrok** to expose a local webhook URL.

```bash
ngrok http <port_number>
```

Add this snippet to the end of `recieveMsg.py`:
```python
if __name__ == "__main__":
    app.run(port=<port_number>)
```

---
##  Hosting on PythonAnywhere
### Deployment Steps
1. Go to the Web Tab.
2. Add a new web app.
3. Select Manual configuration.
4. Choose python version
5. Check version using `python --version`
6. Create a web app
7. Go to console tab.

8. Create a virtual environment in **Console → Bash**
```bash
mkvirtualenv env_name --python=/usr/bin/pythonX.X
```

9. Install dependencies inside the venv:
```bash
pip install -r requirements.txt
```

10. In the **Web** tab, set the project working directory and source code path.

11. Configure the **WSGI file**:
```python
import sys
project_home = "<your_project_path>"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from recieveMsg import app as application
```

12. Set the virtual environment path.
13. In Twilio Sandbox settings, configure webhook URL:
```
https://<username>.pythonanywhere.com/whatsapp
```
14. Click **Reload** on PythonAnywhere to apply changes.

✔ **Deployment complete — your app is now live!**

---
## Testing Commands
```
ADD Rahul 24 May
SHOW Rahul
UPDATE Rahul 25 May
DELETE Rahul
CLEAR
```

---
## License
This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---
## Credits
Developed by **Rahul Naik**

If you use this project, please provide credit by linking back to this repository.

Thank you.
