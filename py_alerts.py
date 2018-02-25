import os
import sys
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.utils import make_msgid
from email.utils import formatdate

class email_alert():

	def __init__(self, config_file='settings.json'):
		try:
			config = json.load(open(config_file))
			self.gmail_user = config['email']['gmail_user']
			self.gmail_pass = config['email']['gmail_pass']
			self.gmail_name = config['email']['gmail_name']
			self.recipients = config['email']['recipients']
		except Exception as e:
			print("Error: settings.json file not found or formatted incorrectly.")

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

		try:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(self.gmail_user, self.gmail_pass)
			server.sendmail(self.gmail_user, self.recipients, email.as_string())
			server.quit()
		except Exception as e:
			print("Failed to send email: " + str(e))

class slack_alert():
	
	def __init__(self, config_file='settings.json'):
		try:
			config = json.load(open(config_file))
			self.webhook = config['slack']['webhook']
		except Exception as e:
			print("Failed to load settings.json file:" + str(e))
			sys.exit(1)

	def send(self, message=None, image=None, filename=None):
		try:
			slack_msg = json.dumps({"text": "{0}".format(message)})
			req = requests.post(self.webhook, data=slack_msg.encode('ascii'),
									headers={'Content-Type': 'application/json'}) 
		except Exception as e:
			print("Failed to send Slack message: " + str(e))
