# Result Update Notifier

This project automatically checks my college exam results website every hour and sends me an email notification if new results are posted.

## Features

- Runs automatically every hour using GitHub Actions
- Scrapes my college results page for updates
- Stores the last checked result to avoid duplicate notifications
- Sends an email notification when new results appear

## How It Works

1. GitHub Actions runs the Python script every hour.
2. The script fetches and parses the results page.
3. If a new result is found, I will receive an email alert.

## Setup

1. **Clone this repository**
2. **Add your email credentials as GitHub repository secrets:**
   - `EMAIL_FROM`
   - `EMAIL_TO`
   - `EMAIL_PASSWORD` (use a Gmail App Password)
3. **Edit the script** (`main.py`) with your college results URL and form data.
4. **Push your changes** to GitHub. The workflow will start automatically.

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

## License

MIT

