import os
import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect

DATABASE = 'pftp.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
  return 'This is Programming Feel The Power'

@app.route('/practice/ex<int:ex_id>')
def practice(ex_id):
    return render_template('practice.html', ex_id=ex_id)

@app.route('/lessons/<path>')
def lesson(path):
  filepath = os.path.join('gen', path)
  if os.path.exists(os.path.join('templates', filepath)):
    return render_template(filepath)
  else:
    return redirect('/')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
  app.run(debug=True)
