import os
import sys
import sqlite3
from flask import Flask, render_template, redirect, Markup, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required

################################################################################
# Config
################################################################################
app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True
# XXX use environment variables
app.config['SECRET_KEY'] = 'this is the secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pftp.db'


################################################################################
# Database
################################################################################
db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), index = True, unique = True, nullable = False)
  firstname = db.Column(db.String(30), index = True, unique = True, nullable = False)
  lastname = db.Column(db.String(30), index = True, unique = True, nullable = False)
  password = db.Column(db.String(255), nullable = False)
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
      backref=db.backref('users', lazy='dynamic'))
  grades = db.relationship('Grade', backref='grade')

  def is_admin(self):
    return self.has_role("admin")

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

class Assignment(db.Model):
  __tablename__ = 'assignment'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100), index = True, unique = True, nullable = False)
  description = db.Column(db.Text(), nullable = False)
  points = db.Column(db.Integer, nullable = False)
  grades = db.relationship('Grade', backref='assignment')

class Grade(db.Model):
  __tablename__ = 'grade'
  id = db.Column(db.Integer, primary_key = True)
  score = db.Column(db.Integer, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


################################################################################
# Student Routes
################################################################################
@app.route('/')
def index():
  return render_template('course_info.html')

@app.route('/lessons/<path:lesson_path>')
def lesson(lesson_path):
  filepath = os.path.join('gen', lesson_path)
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

@app.route('/dashboard')
@login_required
def dashboard():
  return 'dash'

@app.route('/assignments')
@login_required
def assignments():
  assignments = Assignment.query.all()
  return render_template('assignments.html', assignments=assignments)

################################################################################
# Admin Routes
################################################################################

@app.route('/teacher_dashboard')
@roles_required('admin')
def teacher_dashboard():
  return 'teacher dash'


################################################################################
# Runner
################################################################################
if __name__ == '__main__':
  if len(sys.argv) == 2:
    if sys.argv[1] == 'console':
      import code
      code.interact(local=locals())
    elif sys.argv[1] == 'init':
      db.create_all()

      user_role = Role(name="user")
      admin_role = Role(name="admin")

      admin_user = user_datastore.create_user(email="admin@cramm.it", firstname="Cramm", lastname="It", password="p@ssw0rd")
      admin_user.roles.append(user_role)
      admin_user.roles.append(admin_role)

      test_user1 = user_datastore.create_user(email="test@cramm.it", firstname="Test", lastname="User", password="p@ssw0rd")
      test_user1.roles.append(user_role)
      test_user2 = user_datastore.create_user(email="test2@cramm.it", firstname="Test2", lastname="User2", password="p@ssw0rd")
      test_user2.roles.append(user_role)

      db.session.add(admin_user)
      db.session.add(test_user1)
      db.session.add(test_user2)

      assignment1 = Assignment(name='Homework 1', description='Finish exercises 1-5 before next class',  points=10)
      assignment2 = Assignment(name='Homework 2', description='Finish exercises 6-10 before next class', points=10)
      assignment3 = Assignment(name='Project 1', description='Build a turtle graphics game', points=30)
      assignment4 = Assignment(name='Homework 3', description='Finish exercises 11-15 before next class',  points=10)
      assignment5 = Assignment(name='Homework 4', description='Finish exercises 16-20 before next class', points=10)
      assignment6 = Assignment(name='Project 2', description='Build a Flask app', points=30)
      assignment7 = Assignment(name='Homework 5', description='Finish exercises 21-25 before next class',  points=10)
      assignment8 = Assignment(name='Homework 6', description='Finish exercises 26-30 before next class', points=10)
      assignment9 = Assignment(name='Final Project', description='Build something cool', points=50)

      db.session.add(assignment1)
      db.session.add(assignment2)
      db.session.add(assignment3)
      db.session.add(assignment4)
      db.session.add(assignment5)
      db.session.add(assignment6)
      db.session.add(assignment7)
      db.session.add(assignment8)
      db.session.add(assignment9)

      db.session.commit()
  else:
    app.run(debug=True)
