import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# --- CONFIGURATION ---
RESULTS_URL = "https://results.jntuhceh.ac.in/helper.php?jntuhcehpayOne=loadIntialResults"
FORM_DATA = {
    "examCourse": "btech",
    "examRegulation": "R22"
}

TOP_RESULT_SELECTOR = ".examListHolderOne"  # Update with the actual class
LAST_RESULT_FILE = "last_result.txt"

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

EMAIL_SUBJECT = "New College Exam Result Available!"


def fetch_top_result():
    response = requests.post(RESULTS_URL, data=FORM_DATA)
    soup = BeautifulSoup(response.text, "html.parser")
    top_result_div = soup.select_one(TOP_RESULT_SELECTOR)
    return top_result_div.text.strip() if top_result_div else None

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def load_last_result():
    if not os.path.exists(LAST_RESULT_FILE):
        return None
    with open(LAST_RESULT_FILE, "r") as file:
        return file.read().strip()

def save_last_result(result):
    with open(LAST_RESULT_FILE, "w") as file:
        file.write(result)

def main():
    top_result = fetch_top_result()
    if not top_result:
        print("No result found.")
        return

    last_result = load_last_result()
    if top_result != last_result:
        message = f"New result detected:\n\n{top_result}"
        send_email(message)
        save_last_result(top_result)
        print("Notification sent and result updated.")
    else:
        print("No new result.")

if __name__ == "__main__":
    main()
