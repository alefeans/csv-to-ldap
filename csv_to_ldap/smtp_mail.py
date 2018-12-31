import sys
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SmtpServer:

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = self.smtp_connector()

    def smtp_connector(self):
        try:
            c = smtplib.SMTP(self.host, self.port)
            c.starttls()
            c.login(self.user, self.password)
            print('INFO - SMTP - Authentication Successful')
            return c
        except Exception as e:
            print('ERROR - SMTP - ', e)
            sys.exit()

    def read_template(self, filename='examples/message.txt'):
        try:
            with open(filename, 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content)
        except Exception as e:
            print('ERROR - SMTP - ', e)
            sys.exit()

    def email_constructor(self, entries):
        try:
            msg = MIMEMultipart()
            message_template = self.read_template()
            message = message_template.substitute(NAME=entries['name'],
                                                  LASTNAME=entries['lastname'],
                                                  PASSWORD=entries['password'])
            msg['From'] = self.user
            msg['To'] = entries['email']
            msg['Subject'] = 'User Account Info'
            msg.attach(MIMEText(message, 'plain'))
            return msg
        except Exception as e:
            print('ERROR - SMTP - ', e)     
            sys.exit()

    def send_email(self, entries):
        try:
            email = self.email_constructor(entries)
            self.connection.send_message(email)
            print('INFO - SMTP - Sending account info to {}'.format(entries['email']))
        except Exception as e:
            print('ERROR - SMTP - ', e)
            sys.exit()
