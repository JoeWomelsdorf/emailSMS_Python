from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
import imaplib
from email import encoders
import os
import email
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress
from bs4 import BeautifulSoup
import multiprocessing


class CommManager:
    def __init__(self, phone_num, carrier, email_address, email_password):

        carriers_dict = {"AT&T": ['txt.att.net', 'mms.att.net'],
                         "Verizon": ["vtext.com", "vzwpix.com"],
                         "Sprint": ["messaging.sprintpcs.com", "pm.sprint.com"],
                         "TMobile": ["tmomail.net", "tmomail.net"],
                         "Boost": ["smsmyboostmobile.com", "myboostmobile.com"],
                         "Cricket": ["sms.cricketwireless.net", "mms.cricketwireless.net"],
                         "Virgin Mobile": ["vmobl.com", "vmpix.com"],
                         "US Cellular": ["email.uscc.net", "mms.uscc.net"]}

        self.send_addr = email_address
        self.send_pass = email_password
        self.phone = phone_num
        self.carrier = carrier
        self.receiver_addr_sms = phone_num + "@" + carriers_dict.get(carrier)[0]
        self.receiver_addr_mms = phone_num + "@" + carriers_dict.get(carrier)[1]


    def send_sms(self, subject: str, text=""):

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.send_addr
        message['To'] = self.receiver_addr_sms
        message['Subject'] = subject  # The subject line

        message.attach(MIMEText(text))
        text = message.as_string()

        # Create SMTP session for sending the mail
        try:
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(self.send_addr, self.send_pass)  # login with mail_id and password
            session.sendmail(self.send_addr, self.receiver_addr_sms, text)
            print("[INFO] Message Sent")

            session.quit()
            print("[INFO] Session Terminated")


        except:
            print("[ERROR] Email Credentials Error!")

        finally:
            print("[INFO] Message Successfully Sent")

    def send_mms(self, subject: str, text: str, path=None):

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.send_addr
        message['To'] = self.receiver_addr_mms
        message['Subject'] = str(subject)  # The subject line

        # Adding Text
        message.attach(MIMEText(text))

        # If sending an attachment...
        if path is not None:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(path, "rb").read())
            encoders.encode_base64(part)
            filename = os.path.basename(path)

            part.add_header('Content-Disposition', 'attachment; filename={}'.format(filename))
            message.attach(part)

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(self.send_addr, self.send_pass)  # login with mail_id and password

        text = message.as_string()
        session.sendmail(self.send_addr, self.receiver_addr_mms, text)
        session.quit()

    def check_incoming(self):
        message = []

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.send_addr, self.send_pass)
        mail.list()
        mail.select('inbox')

        (retcode, messages) = mail.search(None, '(UNSEEN)')
        if retcode == 'OK':

            for num in messages[0].split():
                typ, data = mail.fetch(num, '(RFC822)')

                for response_part in data:
                    if isinstance(response_part, tuple):
                        original = email.message_from_bytes(response_part[1])

                        sender = original['From']

                        if sender == (self.receiver_addr_mms or self.receiver_addr_sms):

                            raw_email = data[0][1]
                            raw_email_string = raw_email.decode('utf-8')
                            email_message = email.message_from_string(raw_email_string)
                            for part in email_message.walk():
                                if part.get_content_type() == "text/html":
                                    html = part.get_payload(decode=True).decode('utf-8')
                                    soup = BeautifulSoup(html, 'html.parser')
                                    cars = soup.find_all("td")
                                    for tag in cars:
                                        message.append(str(tag.text.strip()))

                            typ, data = mail.store(num, '+FLAGS', '\\Seen')

        return message
)

