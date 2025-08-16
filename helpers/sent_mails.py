import json
import os

def load_sent_emails(sent_emails_path="sent_emails.json"):
    if os.path.exists(sent_emails_path):
        with open(sent_emails_path, "r") as f:
            return set(json.load(f))
    else:
        return set()

def save_sent_emails(sent_emails, sent_emails_path="sent_emails.json"):
    with open(sent_emails_path, "w") as f:
        json.dump(list(sent_emails), f, indent=2)