import os
import pandas as pd
from openai import OpenAI
from helpers.send_email import send_emails_batch
from helpers.sent_mails import load_sent_emails
from helpers.load_backup import load_backup_dict
from helpers.segregate_companies import segregate_companies
from helpers.generate_email_drafts import generate_email_drafts

# Initialize OpenAI client
# generate the OPEN_API_KEY and store as env variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv("resources/contacts.csv")

backup_file = "gpt_email_response_backup.json"
sent_emails_path = "sent_emails.json"

sent_emails = load_sent_emails(sent_emails_path)

# Step 1. Load backup if exists
backup_dict = load_backup_dict(backup_file)

# Step 2. Determine companies needing new generation
companies_to_generate, companies_in_backup = segregate_companies(df, backup_dict)


print(f" Companies already in backup: {len(companies_in_backup)}")
print(f" Companies to generate: {len(companies_to_generate)}")

# Step 3. Generate emails using gpt/ fetch from backup
backup_dict = generate_email_drafts(companies_to_generate, backup_dict, backup_file)

# Step 6. Proceed to sending emails using backup_dict
send_emails_batch(df, backup_dict, sent_emails, sent_emails_path)
