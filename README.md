# Cold Email Automation Tool

Automate personalized cold-email outreach at scale.  
This tool generates tailored email drafts with OpenAI, attaches your resume, and sends messages via Gmail with built-in batching, backups, and idempotency (no duplicate sends).

---

## Features

- **LLM-generated drafts** per company (subject + body), grounded by the company website.
- **Backup & resume**: JSON backup of generated emails; resumes from disk are attached automatically.
- **Batch send with throttling**: Randomized wait between sends to mimic human behavior.
- **Idempotent sends**: A persistent ledger prevents re-emailing the same address.
- **Composable helpers**: Small modules for generation, cleaning JSON, segmentation, sending, and state.

---

## Repository Structure

```
.
├─ mail_script.py                # Orchestrates the full pipeline
├─ helpers/
│  ├─ clean_json.py             # Cleans fenced/markdown JSON from LLM
│  ├─ generate_email_drafts.py  # Calls OpenAI to create subject/body
│  ├─ load_backup.py            # Loads prior LLM output (if any)
│  ├─ segregate_companies.py    # Splits companies by backup presence
│  ├─ send_email.py             # SMTP email senders + batch control
│  └─ sent_mails.py             # Persistence of already-sent recipients
├─ resources/
│  └─ contacts.csv              # Input contact list (Company, Website, Email)
├─ resume.pdf
├─ gpt_email_response_backup.json   # (auto-created) Generated drafts
└─ sent_emails.json                 # (auto-created) Sent email ledger
```

---

## Prerequisites

- **Python** 3.9+
- **OpenAI** account + API key
- **Gmail** account with **App Passwords** enabled  
  (Google Account → Security → 2-Step Verification → App Passwords → “Mail” on “Other” device)

---

## Installation

```bash
# clone your repo
git clone https://github.com/vedantasthana/Cold-Email-Automation-Tool.git
cd Cold-Email-Automation-Tool

# (optional) create a virtual env
python3 -m venv .venv && source .venv/bin/activate

# install deps
pip install -r requirements.txt
```

> If you don’t yet have a `requirements.txt`, add at minimum:
>
> ```
> openai>=1.30.0
> pandas>=2.0.0
> ```

---

## Configuration

Set the following environment variables:

| Variable            | Required | Description                                                                 |
|---------------------|----------|-----------------------------------------------------------------------------|
| `OPENAI_API_KEY`    | ✅       | OpenAI API key for draft generation.                                       |
| `SENDER_EMAIL`      | ✅       | Your Gmail address used as the sender.                                     |
| `EMAIL_APP_PASSWORD`| ✅       | Gmail App Password (not your normal password).                             |
| `RESUME_FILENAME`   | ❌       | Filename to present for the attachment (defaults to `resume.pdf`).         |

Export them in your shell:

```bash
export OPENAI_API_KEY="sk-..."
export SENDER_EMAIL="you@gmail.com"
export EMAIL_APP_PASSWORD="your-app-password"
export RESUME_FILENAME="Vedant_Asthana_Resume.pdf"
```

---

## Input Data

`resources/contacts.csv` must contain:

```csv
Company,Website,Email
Acme Corp,https://www.acme.com,hr@acme.com
Contoso,https://www.contoso.com,jobs@contoso.com
```

**Required columns**: `Company`, `Website`, `Email`.

---

## How It Works (Pipeline)

1. **Load contacts** from `resources/contacts.csv`.
2. **Load backup** (`gpt_email_response_backup.json`) if available to reuse drafts.
3. **Segregate companies** into:
   - Those **already** having drafts in backup.
   - Those **needing** new drafts.
4. **Generate drafts** for missing companies via OpenAI:
   - Prompts the model to visit/understand the company site (instructional).
   - Returns strict JSON: `{ "<company>": { "subject": "...", "body": "..." } }`
   - Merges into backup JSON on disk.
5. **Send emails** with Gmail SMTP:
   - Attaches resume from `attachments/`.
   - Uses randomized wait (900–1200s) between sends.
   - Records each recipient in `sent_emails.json` to avoid duplicates.

---

## Running

```bash
python mail_script.py
```

- **Generated drafts** stored in `gpt_email_response_backup.json`.
- **Sent recipients** stored in `sent_emails.json`.
- **Attachments** pulled from `attachments/` (default path in `send_email.py`, see below).

---

## Customization

### Resume path / attachment name
- Default resume path: `Vedant_Asthana_Resume.pdf` (in `helpers/send_email.py::send_emails_batch`)
- Change to your file, e.g. `attachments/resume.pdf`, and set a clean `RESUME_FILENAME` env var for a nice display name.

### OpenAI model / prompt
- Model: `gpt-4o` (in `helpers/generate_email_drafts.py`).  
  You may switch to another model name supported by your account.
- Prompt customizations: edit tone, constraints, and signature rules in `generate_email_drafts.py`.

### Throttling
- Wait time currently randomized between **900–1200 seconds** per email (15–20 minutes).  
  Adjust in `helpers/send_email.py` if you need faster/slower cadence.

---

## Gmail Notes

- The code uses `SMTP_SSL` at `smtp.gmail.com:465`.
- Ensure **2-Step Verification** is enabled on your Google account and use an **App Password**.
- Some hosts may block SMTP — run from a network where outbound SMTP is allowed.