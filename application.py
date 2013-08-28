import os
import sys
import sqlite3
from flask import Flask, render_template, redirect, Markup, jsonify, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, current_user

from termcolor import colored

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
  id = db.Column(db.Integer(), primary_key=True)
  email = db.Column(db.String(120), index = True, unique = True, nullable = False)
  firstname = db.Column(db.String(30), index = True, unique = True, nullable = False)
  lastname = db.Column(db.String(30), index = True, unique = True, nullable = False)
  password = db.Column(db.String(255), nullable = False)
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
      backref=db.backref('users', lazy='dynamic'))
  grades = db.relationship('Grade', lazy='dynamic', backref='grade')
  programs = db.relationship('Program', lazy='dynamic', backref='program')

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
  id = db.Column(db.Integer(), primary_key = True)
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
  id = db.Column(db.Integer(), primary_key = True)
  name = db.Column(db.String(100), index = True, unique = True, nullable = False)
  description = db.Column(db.Text(), nullable = False)
  deadline = db.Column(db.DateTime(), nullable = False)
  points = db.Column(db.Integer(), nullable = False)
  grades = db.relationship('Grade', lazy='dynamic', backref='assignment')

class Grade(db.Model):
  __tablename__ = 'grade'
  id = db.Column(db.Integer(), primary_key = True)
  score = db.Column(db.Integer(), nullable = False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  assignment_id = db.Column(db.Integer(), db.ForeignKey('assignment.id'))

class Program(db.Model):
  __tablename__ = 'program'
  id = db.Column(db.Integer(), primary_key = True)
  code = db.Column(db.Text(), nullable = False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Lesson(db.Model):
  __tablename__ = 'lesson'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable=False)
  link = db.Column(db.String(30), nullable=False, index = True)
  sublessons = db.relationship('Sublesson', lazy='dynamic', backref='lesson')

class Sublesson(db.Model):
  __tablename__ = 'sublesson'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  link = db.Column(db.String(30), nullable=False)
  lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))


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

@app.route('/about/')
def about():
  return render_template('about.html')

@app.route('/lessons/')
def lesson_home():
  context = {}
  lessons = map(lambda x: x.__dict__, Lesson.query.all())
  context['lessons'] = lessons
  context['lesson_name'] = 'Lessons'
  return render_template('lesson_home.html', context=context)

@app.route('/lessons/<path:lesson_path>')
def lesson(lesson_path):
  if '.html' in lesson_path:
    filepath = os.path.join('gen', lesson_path)
    if os.path.exists(os.path.join('templates', filepath)):
      return render_template(filepath)
  else:
    lesson = Lesson.query.filter(Lesson.link==lesson_path).first()
    context = {}
    sublessons = map(lambda x: x.__dict__, lesson.sublessons)
    for sublesson in sublessons:
      sublesson['sublesson'] = []
    context['lessons'] = sublessons
    context['lesson_name'] = lesson.name
    return render_template('lesson_home.html', context=context)

  return redirect('/')

@app.route('/practice/ex<int:ex_id>')
def practice(ex_id):
  ex = Exercise.query.get(ex_id)
  if ex is not None:
    ex.hint = Markup(ex.hint)
    return render_template('practice.html', ex=ex)
  else:
    return redirect('/practice/ex1')

@app.route('/workspace/')
def workspace():
  return render_template('workspace.html')

@app.route('/assignments/')
def assignments_home():
  assignments = Assignment.query.all()
  return render_template('assignment_home.html', assignments=assignments)

@app.route('/assignments/<int:assignment_id>')
def assignments(assignment_id):
  assignment = Assignment.query.get(assignment_id)
  if assignment is not None:
    return render_template('assignment.html', assignment=assignment)
  else:
    return redirect('/assignments/1')

@app.route('/dashboard/')
@login_required
def user_dashboard():
  context = {}
  context['total_score'] = 0
  context['total_points'] = 0

  assignment_models = Assignment.query.all()
  assignments = map(lambda x: x.__dict__, assignment_models)

  for assignment in assignments:
    grades = Grade.query.filter_by(assignment_id=assignment['id'], user_id=current_user.id).all()

    if len(grades) == 1:
      grade = grades[0]
      assignment['graded'] = True
      assignment['score'] = grade.score
      context['total_score'] += grade.score
      context['total_points'] += assignment['points']
    else:
      assignment['graded'] = False

  context['assignments'] = assignments

  return render_template('dashboard.html', context=context)


###############################################################################
# Admin Routes
################################################################################

@app.route('/admin/')
@roles_required('admin')
def admin_dashboard():
  student_models = User.query.filter(User.roles.any(Role.name == 'user'))
  assignments = Assignment.query.all()

  students = map(lambda x: x.__dict__, student_models)
  for student in students:
    student['grades'] = []
    student['total_points'] = 0
    student['total_score'] = 0
    for assignment in assignments:
      grade = Grade.query.filter_by(user_id=student['id'], assignment_id=assignment.id).all()
      if len(grade) == 1:
        grade = grade[0].__dict__
        grade['completed'] = True
        grade['points'] = assignment.points
        student['total_points'] += assignment.points
        student['total_score'] += grade['score']
        student['grades'].append(grade)
      else:
        student['grades'].append({'completed': False})

  return render_template('admin/dashboard.html', students=students, assignments=assignments)
