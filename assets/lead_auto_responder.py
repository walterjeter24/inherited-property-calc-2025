import csv
import time
import os
import subprocess
from datetime import datetime

# CONFIGURATION
# Path to the CSV file (Now looks in the SAME folder as this script)
LEADS_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Inherited_Leads.csv")
CHECK_INTERVAL = 60 # Check every minute

def send_instant_sms(phone, name):
    # The "Good Evening" Script (Standardized)
    message = f"Good evening {name}, my name is Walter. I received your inquiry about the inherited property calculator. Do you have a few minutes to chat about a potential cash offer?"
    
    print(f"⚡️ Sending Auto-Response to {name} ({phone})...")
    
    # AppleScript to send via iMessage/SMS
    apple_script = f'''
    tell application "Messages"
        set targetService to 1st account whose service type = SMS
        set targetBuddy to participant "{phone}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    
    try:
        subprocess.run(["osascript", "-e", apple_script], check=True)
        print(f"✅ SENT to {phone}")
        return True
    except Exception as e:
        print(f"❌ Failed to send to {phone}: {e}")
        return False

def monitor_leads():
    print("👀 Lead Auto-Responder Active. Watching for new leads...")
    
    # Simple state tracking (in memory for now, ideally database)
    processed_phones = set()
    
    while True:
        if os.path.exists(LEADS_CSV_PATH):
            with open(LEADS_CSV_PATH, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Assuming CSV has headers: Name, Phone, Email
                    phone = row.get('Phone', '').strip()
                    name = row.get('Name', 'Homeowner').strip()
                    
                    if phone and phone not in processed_phones:
                        # NEW LEAD FOUND
                        print(f"🔔 NEW LEAD DETECTED: {name}")
                        success = send_instant_sms(phone, name)
                        if success:
                            processed_phones.add(phone)
                            
        else:
            print(f"⚠️ Waiting for CSV file at: {LEADS_CSV_PATH}")
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_leads()
