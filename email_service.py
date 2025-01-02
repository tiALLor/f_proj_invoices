import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()


def create_email_message(from_mail: str, to_email: str, subject: str, body: str, filename: str, attachment_path: str) -> MIMEMultipart:

    from_mail = os.getenv("EMAIL")
    to_email = "recipient_email@example.com"
    subject = "Email with Attachment"
    body = "Dear recipient,\n\nPlease find the attached document.\n\nBest regards,\nSender"
    

    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_email
    msg['Subject'] = subject
    
    body = body
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent  
    filename = filename                                                    #"File_name_with_extension"
    attachment_path = attachment_path                                      #"path_to_file/document.pdf"
    attachment = open(attachment_path, "rb") 

    # instance of MIMEBase
    p = MIMEBase('application', 'octet-stream') 

    # change the payload into encoded form 
    p.set_payload((attachment).read())
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    return msg

def send_email(to_email: str, subject: str, body: str, filename: str, attachment_path: str) -> None:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    msg = create_email_message(from_email, to_email, subject, body, filename, attachment_path)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(from_email, to_email, msg,)
        # text = msg.as_string()          
        print("Email sent successfully!")