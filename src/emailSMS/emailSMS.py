from distutils.log import ERROR
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
import imaplib
from email import encoders
import os
import email
from tkinter import E
from typing import final
from bs4 import BeautifulSoup

__version__ = 'dev'


class EmailSMS:
    """A class used to send and receive messages over SMS/MMS email gateways

    """

    def __init__(self, phone_num: str, carrier: str, email_address: str, email_password: str):
        """Parameters

        Args:
            phone_num (str):Phone number to send messages to.  Will also filter received messages
            carrier (str): Carrier, see documentation for additional info
            email_address (str): Email to send/receive from.  It is reccomended to create a dedicated account.
            email_password (str): Password to email account.

        """

        # Common U.S. Carriers and their email gateway addresses
        carriers_dict = {"AT&T": ['txt.att.net', 'mms.att.net'],
                         "Verizon": ["vtext.com", "vzwpix.com"],
                         "Sprint": ["messaging.sprintpcs.com", "pm.sprint.com"],
                         "TMobile": ["tmomail.net", "tmomail.net"],
                         "Boost": ["smsmyboostmobile.com", "myboostmobile.com"],
                         "Cricket": ["sms.cricketwireless.net", "mms.cricketwireless.net"],
                         "Virgin Mobile": ["vmobl.com", "vmpix.com"],
                         "US Cellular": ["email.uscc.net", "mms.uscc.net"]}

        smtp_server_dict = {"gmail": ["smtp.gmail.com", 587, "imap.gmail.com"]}

        autolookup = False
        for i in smtp_server_dict.keys():
            if i in email_address:
                self.smtp_data = smtp_server_dict.get(i)
                autolookup = True
                break

        if not autolookup:
            print(*smtp_server_dict.keys(), sep='\n')
            try:
                self.smtp_data = smtp_server_dict.get(input("Choose an email provider from above: "))
            except KeyError as e:
                raise e

        self.send_addr = email_address
        self.send_pass = email_password
        self.phone = phone_num
        self.carrier = carrier
        self.receiver_addr_sms = phone_num + "@" + carriers_dict.get(carrier)[0]
        self.receiver_addr_mms = phone_num + "@" + carriers_dict.get(carrier)[1]

    def _build_message(self, subject, type, text=""):
        # Building Base MIME message
        message = MIMEMultipart()
        message['From'] = self.send_addr
        if type == "sms":
            message['To'] = self.receiver_addr_sms
        elif type == "mms":
            message['To'] = self.receiver_addr_mms

        message['Subject'] = subject

        # If we have a body to our message
        if text is not None:
            message.attach(MIMEText(text))

        return message

    def _send_message(self, message_text, type):
        try:
            session = smtplib.SMTP(self.smtp_data[0], self.smtp_data[1])
            session.starttls()
            session.login(self.send_addr, self.send_pass)

            if type == "sms":
                session.sendmail(self.send_addr, self.receiver_addr_sms, message_text)
            elif type == "mms":
                session.sendmail(self.send_addr, self.receiver_addr_mms, message_text)

        except smtplib.SMTPException as e:
            raise e

        else:
            session.quit()

    def send_sms(self, subject: str, text: str = None):
        """Will send an SMS message to the configured phone.

        If text argument is not passed in, message will only contain a subject line.

        Args:
            subject (_type_): Subject of message.
            text (str, optional): Body of your message. Defaults to None.
        """
        message = self._build_message(subject, "sms", text)

        # Convert MIME to string for sending
        text = message.as_string()

        # Send Message
        self._send_message(text, "sms")

    def send_mms(self, subject: str, text: str = None, path=None):
        """Will send a MMS message to the configured phone.

        Args:
            subject (str): Subject of message.
            text (str, optional): Body of message. Defaults to None.
            path (str, optional): Send an attachment with message. Defaults to None.
        """
        # Setup Base Message
        message = self._build_message(subject, "mms", text)

        # If sending an attachment...
        if path is not None:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(path, "rb").read())
            encoders.encode_base64(part)
            filename = os.path.basename(path)

            part.add_header('Content-Disposition', 'attachment; filename={}'.format(filename))
            message.attach(part)

        text = message.as_string()

        self._send_message(text, "mms")

    def check_incoming(self, mailbox='inbox'):
        """Check incoming mailboxes for messages from phone

            Will only read unread messages from configured phone number

        Args:
            mailbox (str, optional): Which mailbox to check. Defaults to 'inbox'.

        Returns:
            array: Returns an array of the responses.
        """
        message = []

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.send_addr, self.send_pass)
        mail.list()
        mail.select(mailbox)

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