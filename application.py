import os
import sys
import sqlite3
import datetime
from flask import Flask, render_template, redirect, Markup, jsonify, url_for, request, send_file
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, current_user
from flask.ext.login import logout_user
from flask_security.forms import RegisterForm, TextField, Required

from termcolor import colored

################################################################################
# Config
################################################################################
app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = 'PRODUCTION' not in os.environ
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQL_DATABASE_URI', 'sqlite:///pftp.db')
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/register'
app.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'register.html'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'login.html'
app.config['SECURITY_LOGIN_URL'] = '/login'
# app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'base.html'


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
      backref=db.backref('user', lazy='dynamic'))
  grades = db.relationship('Grade', lazy='dynamic', backref='user')
  programs = db.relationship('Program', lazy='dynamic', backref='user')
  submissions = db.relationship('Submission', lazy='dynamic', backref='user')

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
  id = db.Column(db.Integer(), primary_key = True)
  name = db.Column(db.String(100), index = True, unique = True, nullable = False)
  description = db.Column(db.Text(), nullable = False)
  deadline = db.Column(db.DateTime(), nullable = False)
  points = db.Column(db.Integer(), nullable = False)
  grades = db.relationship('Grade', lazy='dynamic', backref='assignment')
  submissions = db.relationship('Submission', lazy='dynamic', backref='assignment')

class Grade(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  score = db.Column(db.Integer(), nullable = False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  assignment_id = db.Column(db.Integer(), db.ForeignKey('assignment.id'))

class Program(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  title = db.Column(db.Text(), nullable = False, default = 'Untitled Program')
  code = db.Column(db.Text(), nullable = False, default = '')
  last_modified = db.Column(db.DateTime(), nullable = False, default = datetime.datetime.now)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Submission(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  title = db.Column(db.Text(), nullable = False)
  code = db.Column(db.Text(), nullable = False)
  submit_time = db.Column(db.DateTime(), nullable = False, default = datetime.datetime.now)
  assignment_id = db.Column(db.Integer(), db.ForeignKey('assignment.id'))
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Lesson(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  name = db.Column(db.String(30), nullable=False)
  link = db.Column(db.String(30), nullable=False, index = True)
  sublessons = db.relationship('Sublesson', lazy='dynamic', backref='lesson')

class Sublesson(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  link = db.Column(db.String(30), nullable=False)
  lesson_id = db.Column(db.Integer(), db.ForeignKey('lesson.id'))

class Week(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  lesson = db.Column(db.Integer(), db.ForeignKey('lesson.id'))
  assignment = db.Column(db.Integer(), db.ForeignKey('assignment.id'))

class ExtendedRegisterForm(RegisterForm):
  firstname = TextField('First Name', [Required()])
  lastname = TextField('Last Name', [Required()])

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

################################################################################
# Registration Routes
################################################################################
@app.route('/register', methods=['GET'])
def register():
  return render_template('register.html')

################################################################################
# Student Routes
################################################################################
@app.route('/')
def index():
  return redirect('/about/')

@app.route('/about/')
def about():
  weeks = map(lambda x:x.__dict__, Week.query.all())
  # not sure if this is the best way
  for week in weeks:
    week['assignment'] = Assignment.query.get(week['assignment'])
    week['lesson'] = Lesson.query.get(week['lesson'])
  return render_template('about.html', weeks=weeks)

@app.route('/lessons/')
def lesson_home():
  context = {}
  lessons = map(lambda x: x.__dict__, Lesson.query.all())
  context['lessons'] = lessons
  context['lesson_name'] = 'Lessons'
  return render_template('lesson_home.html', context=context)

@app.route('/lessons/<path:lesson_path>')
def lesson(lesson_path):
  file_path = os.path.join('gen', lesson_path)
  if '.pdf' in file_path:
    if os.path.exists(os.path.join('templates', file_path)):
      return send_file(os.path.join('templates', file_path), mimetype='application/pdf')
    else:
      return redirect('/')
  if '.html' in file_path:
    if os.path.exists(os.path.join('templates', file_path)):
      return render_template(file_path)
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
def workspace_home():
  if current_user.is_authenticated():
    programs = Program.query.filter_by(user_id=current_user.id).order_by(Program.last_modified.desc()).all()
    return render_template('workspace_home.html', programs=programs)
  return render_template('workspace.html')

@app.route('/workspace/<int:prog_id>')
@login_required
def workspace(prog_id):
  program = Program.query.filter_by(id=prog_id, user_id=current_user.id).first()
  if program == None:
    return redirect('/workspace/')
  return render_template('workspace.html', program=program)

@app.route('/new_program/')
@login_required
def new_program():
  program = Program(user_id=current_user.id)
  db.session.add(program)
  db.session.commit()
  return redirect('/workspace/'+str(program.id))

@app.route('/save_program/', methods=['POST'])
@login_required
def save_program():
  title = request.form['title']
  code = request.form['code']
  program = None
  if 'program_id' in request.form:
    program = Program.query.filter_by(id=request.form['program_id'], user_id=current_user.id).first()
    program.title = title
    program.code = code
    program.last_modified = datetime.datetime.now()
  else:
    program = Program(title=title, code=code, user_id=current_user.id)
  db.session.add(program)
  db.session.commit()
  return str(program.id)

@app.route('/delete_program/', methods=['POST'])
@login_required
def delete_program():
  program = Program.query.filter_by(id=request.form['program_id'], user_id=current_user.id).first()
  db.session.delete(program)
  db.session.commit()
  return ''

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

@app.route('/cheatsheet.html')
def cheatsheet():
  return render_template('cheatsheet.html')

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
    else:
      assignment['graded'] = False
    context['total_points'] += assignment['points']

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
      if len(grade) >= 1:
        # take the most recently updated grade
        grade = grade[-1].__dict__
        grade['completed'] = True
        grade['points'] = assignment.points
        student['total_points'] += assignment.points
        student['total_score'] += grade['score']
        student['grades'].append(grade)
      else:
        student['grades'].append({'completed': False})

  return render_template('admin/dashboard.html', students=students, assignments=assignments)


@app.route('/admin/submit_grade/', methods=['POST'])
@roles_required('admin')
def submit_grade():
  assignment = Assignment.query.filter(Assignment.name==request.json['assignment_name']).first()
  first_name = request.json['student_name'].rsplit(' ', 1)[0]
  last_name = request.json['student_name'].rsplit(' ', 1)[1]
  student = User.query.filter(User.firstname==first_name and User.lastname==last_name).first()
  student.add_grade(assignment, int(request.json['score']))
  return "success"
