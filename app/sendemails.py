import smtplib
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

def send_email(user_email, alert_id, alert_target):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL, PASSWORD)
        subject = f"Your Alert has hit the target!"
        body = f"Alert: {alert_id} has been triggered! React soon. Bitcoin is at: {alert_target}"
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL, user_email, msg)
        print("Sent Mail")

