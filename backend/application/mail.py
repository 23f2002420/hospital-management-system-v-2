import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "hms@donotreply.in"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message, content = "html", attachment_filename = None, attachment_file_content=None):
    print(f"---Attempting to send email to {to_address} ---")
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment_filename and attachment_file_content:
        print(f"---Attaching file: {attachment_filename} ---")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment_file_content.encode('utf-8'))
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment_filename}")
        msg.attach(part)
    try:
        print(f"---Connecting to SMTP server {SMTP_SERVER_HOST}:{SMTP_SERVER_PORT}---")   
        s = smtplib.SMTP(host = SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)
        # s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        print("----Sending message ----")
        s.send_message(msg)
        print(f"---Message send, quitting SMTP----")
        s.quit()
        print(f"Emails successfully sent to {to_address} ---")
        return True
    except Exception as e:
        print(f"Error within send_email function: {e}")
        return False