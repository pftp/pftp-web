import os
import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, g, Markup
from flask.ext.sqlalchemy import SQLAlchemy

################################################################################
# Config
################################################################################
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pftp.db'

################################################################################
# Database
################################################################################
db = SQLAlchemy(app)

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(120), index = True, unique = True, nullable = False)
  firstname = db.Column(db.String(30), index = True, unique = True, nullable = False)
  lastname = db.Column(db.String(30), index = True, unique = True, nullable = False)
  role = db.Column(db.SmallInteger, default = ROLE_USER, nullable = False)

  def __init__(self, firstname, lastname, email, role=ROLE_USER):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.role = role

  def __repr__(self):
    return '<User %r>' % (self.email)

class Exercise(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  prompt = db.Column(db.Text(), nullable = False)
  hint = db.Column(db.Text(), nullable = False)
  test_cases = db.Column(db.Text(), nullable = False)
  solution = db.Column(db.Text(), nullable = False)

  def __init__(self, prompt, hint, test_cases, solution):
    self.prompt = prompt
    self.hint = hint
    self.test_cases = test_cases
    self.solution = solution

  def __repr__(self):
    return '<Exercise %r>' % (self.prompt)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


################################################################################
# Routes
################################################################################
@app.route('/')
def index():
  return render_template('course_info.html')

@app.route('/lessons/<path>')
def lesson(path):
  filepath = os.path.join('gen', path)
  if os.path.exists(os.path.join('templates', filepath)):
    return render_template(filepath)
  else:
    return redirect('/')

@app.route('/practice/ex<int:ex_id>')
def practice(ex_id):
    ex = Exercise.query.get(ex_id)
    if ex is not None:
        ex.hint = Markup(ex.hint)
        return render_template('practice.html', ex=ex)
    else:
        return redirect('/practice/ex1')


################################################################################
# Runner
################################################################################
if __name__ == '__main__':
  app.run(debug=True)
