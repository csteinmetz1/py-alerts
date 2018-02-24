import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.utils import make_msgid
from email.utils import formatdate

class email_alert():

	def __init__(self, config_file='settings.json'):
		config = json.load(open(config_file))
		self.gmail_user = config['gmail_user']
		self.gmail_pass = config['gmail_pass']
		self.gmail_name = config['gmail_name']
		self.recipients = config['recipients']

	def send(self, subject=None, message=None, image=None, filename=None):

		email = MIMEMultipart()
		email['From'] = formataddr((self.gmail_name, self.gmail_user))
		email['To'] = ", ".join(self.recipients)
		email['Subject'] = subject
		
		if message:
			email.attach(MIMEText(message))
		if image:
			email.attach(MIMEImage(file(image).read()))
		if filename:
			part = MIMEApplication(file(filename).read())
			part.add_header('Content-Disposition', 
			'attachment; filename="%s"' % os.path.basename(filename))
			email.attach(part)

		text = email.as_string()
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(self.gmail_user, self.gmail_pass)
		server.sendmail(self.gmail_user, self.recipients, text)
		server.quit()

email_alert().send(subject="This is the subject", message="This is the body of the email")