import base64
import hashlib
import hmac
from passlib.hash import bcrypt

password_salt = '$2a$12$skCRnkqE5L01bHEke678Ju'

def get_hmac(password):
  h = hmac.new(password_salt, password.encode('utf-8'), hashlib.sha512)
  return base64.b64encode(h.digest())

def encrypt_password(password):
  return bcrypt.encrypt(get_hmac(password))
