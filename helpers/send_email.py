import os
import smtplib
import random
import time
from helpers.sent_mails import save_sent_emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(recipient, subject, body, resume_path):
    # Generate from Google App Passwords
    # save your filename, email and app password in env variables SENDER_EMAIL and EMAIL_APP_PASSWORD
    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("EMAIL_APP_PASSWORD")
    resume_filename = os.environ.get("RESUME_FILENAME", "resume.pdf")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Subject"] = subject

    # Attach mail body
    msg.attach(MIMEText(body, "plain"))

    # Attach your resume
    with open(resume_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header("Content-Disposition", "attachment", filename=resume_filename)
        msg.attach(attach)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print(f" Email sent to {recipient}")

curr_dir = os.getcwd()
resume_path = curr_dir + '/Vedant_Asthana_SDE.pdf'

def send_emails_batch(df, backup_dict, sent_emails, sent_emails_path, resume_path=resume_path):
    for index, row in df.iterrows():
        email_id = row["Email"]
        company_name = row["Company"]

        if email_id in sent_emails:
            print(f"Skipping {email_id} (already sent)")
            continue

        email_info = backup_dict.get(company_name, {})
        subject = email_info.get("subject", "Introduction: Recent NYU CS Graduate Seeking Opportunities")
        body = email_info.get("body", "")

        if body:
            print(f"Sending email to: {email_id} (Company: {company_name})")
            send_email(
                recipient=email_id,
                subject=subject,
                body=body,
                resume_path=resume_path
            )

            sent_emails.add(email_id)
            save_sent_emails(sent_emails, sent_emails_path)

            wait_time = random.randint(900, 1200)
            print(f"Waiting {wait_time} seconds before next email...\n")
            time.sleep(wait_time)
        else:
            print(f"No email draft found for {company_name}")