# AI Job Outreach Agent 🤖✉️

A Python-based AI-powered automation tool that helps job seekers send emails to companies, track responses, and classify replies using AI for better follow-up management.

---

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [Folder Structure](#folder-structure)  
5. [Security](#security)  
6. [Future Enhancements](#future-enhancements)  
7. [License](#license)  
8. [Demo](#demo)  

---

## Features

- **Automated Email Sending**: Sends personalized emails to company contacts using Gmail.  
- **Reply Tracking**: Reads unread replies from your Gmail inbox and matches them with the sent emails.  
- **AI Classification**: Classifies responses as `positive`, `neutral`, `interview`, `auto_reply`, or `rejection` using AI (Google Gemini API).  
- **Database Management**: Tracks sent emails, reply status, and AI classification in a local SQLite database (`emails.db`).  
- **Quick Testing Mode**: Simulate replies to test AI classification without sending real emails.  
- **Secure Environment**: Credentials and sensitive data are stored securely using environment variables (`.env`), not committed to GitHub.  
- **Extensible**: Modular Python code, making it easy to add new email providers or AI models.  

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-job-agent.git
cd ai-job-agent
```

2. Create a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup Environment Variables
- Create a .env file in the root folder with your Gmail credentials and Google API keys.
- Example:
```bash
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```
## Usage
Run the agent
```bash
python main.py
```
Run with shell script
```bash
./run_agent.sh
```
Check the database
```bash
from modules.db_handler import fetch_all
print(fetch_all())
```
Simulate replies for testing
```bash
test_replies = [
    {"company": "testcompany1", "email": "example1@gmail.com", "body": "We would like to schedule an interview."},
    {"company": "testcompany2", "email": "example2@gmail.com", "body": "Unfortunately, we are not moving forward."}
]
```

## Folder Structure
```bash
ai-job-agent/
├─ main.py                # Main script to run the agent
├─ run_agent.sh           # Shell script to run agent
├─ modules/               # Python modules
│  ├─ email_sender.py
│  ├─ email_reader_gmail.py
│  ├─ db_handler.py
│  ├─ ai_gemini.py
│  └─ auto_responder.py
├─ data.csv               # Local CSV (ignored in Git)
├─ emails.db              # SQLite database
├─ venv/                  # Python virtual environment
├─ credentials.json       # OAuth credentials (ignored in Git)
└─ requirements.txt       # Python dependencies
```
## Security
- No secrets in Git: data.csv, credentials, and OAuth keys are .gitignored.
- Local SQLite database: All email tracking happens locally.
- Environment Variables: Sensitive info like emails and API keys never exposed.
  
## Future Enhancements
- Multi-platform email support (Outlook, LinkedIn).
- Integration with AI for automated follow-ups and prioritization.
- Web dashboard to visualize sent emails and AI classification.
- Scheduled job execution for continuous outreach.
- 
## License
MIT License © 2026 [Joel Chirayath]
