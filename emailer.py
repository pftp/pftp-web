import os
import sys
import smtplib
from termcolor import colored
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from application import User, db, Role

class Emailer:
  def __init__(self): 
    # get email credentials
    if 'EMAIL_PASSWORD' in os.environ and 'EMAIL_ADDRESS' in os.environ:
      self.address = os.environ.get('EMAIL_ADDRESS')
      password = os.environ.get('EMAIL_PASSWORD')
      # setup mailer
      self.mail_server = smtplib.SMTP("smtp.gmail.com", 587)
      self.mail_server.starttls()
      self.mail_server.login(self.address, password)
    else:
      print colored('ERROR: set environment variable EMAIL_ADDRESS AND EMAIL_PASSWORD', 'red')

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.mail_server.quit() 

  def email_user(self, email, name, subject, text):
    msg = MIMEMultipart()
    msg['From'] = self.address
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    self.mail_server.sendmail(self.address, email, msg.as_string())
    print colored("SENT ONE EMAIL TO " + email, 'green')

"""
Usage:
if __name__ == '__main__':
  with Emailer() as emailer:
    emailer.email_user('admin@cramm.it', 'Testname', 'testsubject', 'testteset')
"""
