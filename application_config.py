from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = 'PRODUCTION' not in os.environ
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQL_DATABASE_URI', 'sqlite:///pftp.db')
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$12$skCRnkqE5L01bHEke678Ju'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/register'
app.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'register.html'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'login.html'
app.config['SECURITY_LOGIN_URL'] = '/login'
app.config['SECURITY_CHANGEABLE'] = True
# app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'base.html'

# Fake emails for now
class FakeMail(object):
  def send(self, message):
    pass

app.extensions = getattr(app, 'extensions', {})
app.extensions['mail'] = FakeMail()

################################################################################
# Database
################################################################################
db = SQLAlchemy(app)
