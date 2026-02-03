import smtplib
import os # <--- Import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv() # Load environment variables

def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email - EduFlow"
    msg["From"] = os.getenv("MAIL_USERNAME") # <--- Use env var
    msg["To"] = to_email
    msg.set_content(f"""
Your OTP for email verification is:

{otp}

This OTP is valid for 10 minutes.
""")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(
            os.getenv("MAIL_USERNAME"), 
            os.getenv("MAIL_PASSWORD")
        )
        server.send_message(msg)