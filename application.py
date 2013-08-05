import os
import sys
import sqlite3
from flask import Flask, render_template, redirect, Markup, jsonify, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, current_user

################################################################################
# Config
################################################################################
app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = 'PRODUCTION' not in os.environ
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQL_DATABASE_URI', 'sqlite:///pftp.db')


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
  grades = db.relationship('Grade', lazy='dynamic', backref='grade')

  def is_admin(self):
    return self.has_role("admin")

  def add_grade(self, assignment, score):
    grade = Grade(score=score)
    self.grades.append(grade)
    assignment.grades.append(grade)
    db.session.add(grade)
    db.session.commit()

  def get_grade(self, assignment):
    grades = self.grades.filter_by(assignment_id=assignment.id).all()
    if len(grades) == 0:
      grade = self.grades.filter_by(assignment_id=assignment.id).all()[0]
      return grade
    else:
      return None

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
  grades = db.relationship('Grade', lazy='dynamic', backref='assignment')

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
  if current_user.is_authenticated():
    if current_user.is_admin():
      return redirect(url_for('admin_dashboard'))
    else:
      return redirect(url_for('user_dashboard'))
  else:
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
def user_dashboard():
  grade_models = Grade.query.filter_by(user_id=current_user.id)

  grades = map(lambda x: x.__dict__, grade_models)
  for grade in grades:
    assignment = Assignment.query.filter_by(id=grade['assignment_id']).all()[0]

    grade['assignment'] = assignment

  return render_template('dashboard.html', assignments=assignments, grades=grades)

@app.route('/assignments')
@login_required
def assignments():
  assignments = Assignment.query.all()
  return render_template('assignments.html', assignments=assignments)

################################################################################
# Admin Routes
################################################################################

@app.route('/admin')
@roles_required('admin')
def admin_dashboard():
  student_models = User.query.filter(User.roles.any(Role.name == 'user'))
  assignments = Assignment.query.all()
  grades = Grade.query

  students = map(lambda x: x.__dict__, student_models)
  for student in students:
    student['grades'] = map(lambda x: x.__dict__, grades.filter_by(user_id=student['id']))

  return render_template('admin/dashboard.html', students=students, assignments=assignments)
