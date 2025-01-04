import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
from email.message import EmailMessage

load_dotenv()


def create_email_message(
    from_mail: str,
    to_email: str,
    subject: str,
    body: str,
    filename: str,
    attachment_path: str,
) -> MIMEMultipart:
    
    msg = EmailMessage()
    msg["From"] = from_mail
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = filename

    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    return msg


def send_email(
    to_email: str, subject: str, body: str, filename: str, attachment_path: str
) -> None:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    msg = create_email_message(from_email, to_email, subject, body, filename, attachment_path)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        # s.sendmail(mail_from, mail_to, msg.encode('utf-8'))
        # text = msg.as_string()
        print("Email sent successfully!")



if __name__ == "__main__":
    send_email(
        to_email="tibor.bebjak@gmail.com",
        subject="Test",
        body="Test",
        filename="Invoice 000003.pdf",
        attachment_path="PDF_invoice\\Invoice 000003.pdf",
    )