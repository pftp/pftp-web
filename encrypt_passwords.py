import base64
import hashlib
import hmac
import sqlite3
from passlib.hash import bcrypt

password_salt = '$2a$12$skCRnkqE5L01bHEke678Ju'

def get_hmac(password):
  h = hmac.new(password_salt, password.encode('utf-8'), hashlib.sha512)
  return base64.b64encode(h.digest())

def encrypt_password(password):
  return bcrypt.encrypt(get_hmac(password))

db = sqlite3.connect('pftp_prod.db')
users = db.execute('select id, password from user;')
for user in users:
  new_password = encrypt_password(user[1])
  db.execute('update user set password=? where id=?', [new_password, user[0]])
db.commit()
db.close()
