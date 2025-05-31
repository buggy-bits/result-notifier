import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import hashlib

# --- CONFIGURATION ---
RESULTS_URL = "https://results.jntuhceh.ac.in/helper.php?jntuhcehpayOne=loadIntialResults"
FORM_DATA = {
    "examCourse": "btech",
    "examRegulation": "R22"
}
TOP_RESULT_SELECTOR = ".examListHolderOne"
LAST_RESULT_FILE = "last_result.txt"
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO") 
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_SUBJECT = "New College Exam Result Available!"

def fetch_top_result():
    # Because that website will show the latest result on the top div
    try:
        response = requests.post(RESULTS_URL, data=FORM_DATA, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        top_result_div = soup.select_one(TOP_RESULT_SELECTOR)
        return top_result_div.text.strip() if top_result_div else None
    except requests.RequestException as e:
        print(f"Error fetching results: {e}")
        return None

def send_email(message):
    
    try:
        msg = MIMEText(message)
        msg["Subject"] = EMAIL_SUBJECT
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def load_last_result():
    """Load the last result from cache file"""
    if not os.path.exists(LAST_RESULT_FILE):
        print("No previous result found")
        return None
    
    try:
        with open(LAST_RESULT_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading last result: {e}")
        return None

def save_last_result(result):
    # Save the current result to cache file
    # again after the program has run, github action script will cache the file
    try:
        with open(LAST_RESULT_FILE, "w", encoding="utf-8") as file:
            file.write(result)
        print(f"Result saved to {LAST_RESULT_FILE}")
    except Exception as e:
        print(f"Error saving result: {e}")

def get_result_hash(result):
    return hashlib.md5(result.encode('utf-8')).hexdigest()

def main():
    print("Checking for new college results...")
    
    # Fetch current result
    current_result = fetch_top_result()
    if not current_result:
        print("Failed to fetch current result")
        return
    
    print(f"Current result preview: {current_result[:100]}...")
    
    # Load last result
    last_result = load_last_result()
    
    # Compare results
    if last_result is None:
        # First run - save current result
        save_last_result(current_result)
    elif current_result != last_result:
        # New result detected
        
        message = f"""New college exam result detected!
Hello,
Latest result:
{current_result}

Check the results page: {RESULTS_URL}
"""
        
        if send_email(message):
            print("📧 Email notification sent successfully")
        else:
            print("❌ Failed to send email notification")
        
        # Save new result
        save_last_result(current_result)
        print("✅ Result cache updated")
        
        # Set output for GitHub Actions
        if os.environ.get("GITHUB_ACTIONS"):
            with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
                f.write("new_result=true\n")
    else:
        print("No new results - current result matches cached result")

if __name__ == "__main__":
    main()