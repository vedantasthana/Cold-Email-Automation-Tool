import os
import json

def load_backup_dict(backup_file="response_backup.json"):
    if os.path.exists(backup_file):
        with open(backup_file, "r") as f:
            print("Loaded existing backup file.")
            return json.load(f)
    else:
        print("Backup file not found. Starting fresh.")
        return {}