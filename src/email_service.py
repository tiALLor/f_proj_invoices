import smtplib
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
) -> EmailMessage:
    if from_mail is None:
        raise ValueError(
            "Sender email (FROM_EMAIL) is not configured in environment variables."
        )

    msg = EmailMessage()
    msg["From"] = from_mail
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with open(attachment_path, "rb") as f:
            file_data = f.read()

        # The modern API automatically figures out the MIME type from the file data/filename,
        # but specifying the subtype as 'octet-stream' is robust for generic files (like PDFs).
        msg.add_attachment(
            file_data, maintype="application", subtype="octet-stream", filename=filename
        )
    except FileNotFoundError:
        print(f"Error: Attachment file not found at path: {attachment_path}")
        # Depending on requirements, might want to send the email without the attachment?,
        # or raise an exception to stop the process. Here, we raise.
        raise
    return msg


def send_email(
    to_email: str, subject: str, body: str, filename: str, attachment_path: str
) -> None:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    if not from_email or not password:
        print("Error: EMAIL or PASSWORD environment variable not set.")
        return

    try:
        msg = create_email_message(
            from_email, to_email, subject, body, filename, attachment_path
        )
    except Exception as e:
        print(f"Could not prepare email message: {e}")
        return

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)

            # send_message is the correct method for EmailMessage objects
            server.send_message(msg)

            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print(
            "Error: SMTP Authentication Failed. Check username/password or 'Less secure app access'/'App Passwords' settings."
        )
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    send_email(
        to_email="tibor.bebjak@gmail.com",
        subject="Test",
        body="Test",
        filename="Invoice 000003.pdf",
        attachment_path="src/PDF_invoice/Invoice 000003.pdf",
    )
