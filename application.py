import os, sys, sqlite3, datetime, json, subprocess, pipes, uuid, shutil, cgi
from flask import Flask, render_template, redirect, Markup, jsonify, url_for, request, send_file, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, current_user
from flask.ext.security.signals import user_registered
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
  firstname = db.Column(db.String(30), index = True, nullable = False)
  lastname = db.Column(db.String(30), index = True, nullable = False)
  password = db.Column(db.String(255), nullable = False)
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
      backref=db.backref('user', lazy='dynamic'))
  grades = db.relationship('Grade', lazy='dynamic', backref='user')
  programs = db.relationship('Program', lazy='dynamic', backref='user')
  code_revisions = db.relationship('CodeRevision', lazy='dynamic', backref='user')
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

  def to_dict(self):
    return {
        'name': self.name,
        'description': self.description,
        'deadline': str(self.deadline),
        'points': self.points
        }

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
  code_revisions = db.relationship('CodeRevision', lazy='dynamic', backref='program')

class LabProgram(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  section = db.Column(db.Integer(), nullable = False)
  lab_id = db.Column(db.Integer(), nullable = False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  program_id = db.Column(db.Integer(), db.ForeignKey('program.id'))

class CodeRevision(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  title = db.Column(db.Text(), nullable = False)
  diff = db.Column(db.Text(), nullable = False)
  time = db.Column(db.DateTime(), nullable = False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  program_id = db.Column(db.Integer(), db.ForeignKey('program.id'))

class CodeRun(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  title = db.Column(db.Text(), nullable = False)
  code = db.Column(db.Text(), nullable = False)
  output = db.Column(db.Text())
  error = db.Column(db.Text())
  time = db.Column(db.DateTime(), nullable = False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  program_id = db.Column(db.Integer(), db.ForeignKey('program.id'))

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

  def to_dict(self):
    return {
        'name': self.name,
        'link': self.link,
        'sublessons': map(lambda x: x.to_dict(), self.sublessons)
        }

class Sublesson(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  link = db.Column(db.String(30), nullable=False)
  lesson_id = db.Column(db.Integer(), db.ForeignKey('lesson.id'))

  def to_dict(self):
    return {
        'name': self.name,
        'link': self.link
        }

class Week(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  lesson = db.Column(db.Integer(), db.ForeignKey('lesson.id'))
  assignment = db.Column(db.Integer(), db.ForeignKey('assignment.id'))

  def to_dict(self):
    return {
        'lesson': self.lesson,
        'assignment': self.assignment.to_dict()
        }

class ExtendedRegisterForm(RegisterForm):
  firstname = TextField('First Name', [Required()])
  lastname = TextField('Last Name', [Required()])

class Quiz(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  week = db.Column(db.Integer(), nullable=False)
  questions = db.relationship('QuizQuestion', lazy='dynamic', backref='quiz')

  def to_dict(self):
    return {
        'name': self.name,
        'questions': map(lambda x: x.to_dict(), self.questions)
        }

class QuizQuestion(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  question = db.Column(db.String(1000), nullable=False)
  answer_choices = db.Column(db.String(7000), nullable=False)
  solution = db.Column(db.String(100), nullable=False)
  quiz_id = db.Column(db.Integer(), db.ForeignKey('quiz.id'))
  def to_dict(self):
    return {'question': self.question, 'answer_choices': self.answer_choices, 'solution': self.solution, 'quiz_id': self.quiz_id}

class QuizResponse(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  question_id = db.Column(db.Integer(), db.ForeignKey('quiz_question.id'), nullable=False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
  user_answer = db.Column(db.String(100), nullable=False)

class PracticeProblemTemplate(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  problem_dir = db.Column(db.String(20), nullable=False)

class PracticeProblem(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  template_id = db.Column(db.Integer(), db.ForeignKey('practice_problem_template.id'), nullable=False)
  prompt = db.Column(db.String(500), nullable=False)
  expected = db.Column(db.String(500), nullable=False)
  solution = db.Column(db.String(500), nullable=False)
  test = db.Column(db.String(500), nullable=False)

class PracticeProblemSubmissions(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  problem_id = db.Column(db.Integer(), db.ForeignKey('practice_problem.id'))
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
  default_role = user_datastore.find_role("user")
  user_datastore.add_role_to_user(user, default_role)
  db.session.commit()

################################################################################
# Registration Routes
################################################################################
@app.route('/register', methods=['GET'])
def register():
  return render_template('register.html')

################################################################################
# Settings Routes
################################################################################
@app.route('/settings', methods=['GET'])
def register():
  return render_template('settings.html')

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
    quiz = Quiz.query.filter(Quiz.week==week['id'])
    if len(quiz.all()) == 1:
      week['quiz'] = quiz.first()
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

@app.route('/quiz/<int:quiz_id>/')
def quiz(quiz_id):
  #if not current_user.is_authenticated():
  #  return render_template('message.html', message='You need to log in first')
  first_quiz = Quiz.query.filter(Quiz.week==quiz_id).first()
  questions = map(lambda x: x.__dict__, first_quiz.questions)
  for question in questions:
    question['answer_choices'] = json.loads(question['answer_choices'])
  first_quiz = first_quiz.__dict__
  first_quiz['questions'] = questions
  return render_template('quiz.html', quiz=first_quiz)


@app.route('/quiz/<int:quiz_id>/submit/', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
  answer_choices = request.form.getlist('selected[]')
  for answer_choice in answer_choices:
    question_id, answer = answer_choice.strip().split(',')
    qr = QuizResponse(question_id=int(question_id), user_id=current_user.id, user_answer=answer)
    db.session.add(qr)
  db.session.commit()
  return 'Submitted'


@app.route('/labs/<int:lab_id>')
def lab(lab_id):
  section = 0
  program = None
  if current_user.is_authenticated():
    lab_program = LabProgram.query.filter_by(lab_id=lab_id, user_id=current_user.id).first()
    if lab_program != None:
      section = lab_program.section
      program = Program.query.filter_by(id=lab_program.program_id, user_id=current_user.id).first()
  if program != None:
    return render_template('lab.html', lab_id=lab_id, section=section, program=program)
  return render_template('lab.html', lab_id=lab_id, section=section)

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

@app.route('/workspace/<int:program_id>')
@login_required
def workspace(program_id):
  program = Program.query.filter_by(id=program_id, user_id=current_user.id).first()
  if program == None:
    return redirect('/workspace/')
  return render_template('workspace.html', program=program)

@app.route('/workspace/<int:program_id>/revision/<int:revision_id>')
@login_required
def program_revision(program_id, revision_id):
  program = Program.query.filter_by(id=program_id, user_id=current_user.id).first()
  if program == None:
    return redirect('/workspace/')
  target_revision = CodeRevision.query.filter_by(id=revision_id, program_id=program.id, user_id=current_user.id).first()
  if target_revision == None:
    return redirect('/workspace/' + str(program.id))
  revisions = CodeRevision.query.order_by(CodeRevision.time).filter(CodeRevision.time <= target_revision.time).all()
  codelines = ['']
  for revision in revisions:
    diff = json.loads(revision.diff)
    old_code = diff['old_code']
    old_code.reverse()
    for removal in old_code:
      del codelines[removal['linenum']-1]
    for addition in diff['new_code']:
      codelines.insert(addition['linenum']-1, addition['code'])
  program.code = '\n'.join(codelines)
  return render_template('workspace.html', program=program)

@app.route('/new_program/')
@login_required
def new_program():
  program = Program(user_id=current_user.id)
  db.session.add(program)
  db.session.commit()
  return redirect('/workspace/'+str(program.id))

def compute_diff(old_code, new_code):
  memo = {}

  def lcs_lines(old_lines, new_lines):
    if len(old_lines) == 0 or len(new_lines) == 0:
      return []
    elif (len(old_lines), len(new_lines)) in memo:
      return memo[(len(old_lines), len(new_lines))]
    res = None
    if old_lines[-1]['code'] == new_lines[-1]['code']:
      common_line = {
        'old_num': old_lines[-1]['linenum'],
        'new_num': new_lines[-1]['linenum']
      }
      res = lcs_lines(old_lines[:-1], new_lines[:-1]) + [common_line]
    else:
      left_res = lcs_lines(old_lines[:-1], new_lines)
      right_res = lcs_lines(old_lines, new_lines[:-1])
      res = left_res if len(left_res) >= len(right_res) else right_res
    memo[(len(old_lines), len(new_lines))] = res
    return res

  old_code_split = old_code.split('\n')
  new_code_split = new_code.split('\n')
  old_code_lines = [{'code': line, 'linenum': i + 1} for i,line in enumerate(old_code_split)]
  new_code_lines = [{'code': line, 'linenum': i + 1} for i,line in enumerate(new_code_split)]
  common_lines = lcs_lines(old_code_lines, new_code_lines)
  common_lines.append({
    'old_num': len(old_code_lines) + 1,
    'new_num': len(new_code_lines) + 1
  })
  diff = {'old_code': [], 'new_code': []}
  cur_old_num = 1
  cur_new_num = 1
  for line in common_lines:
    if line['old_num'] > cur_old_num:
      diff['old_code'] += old_code_lines[cur_old_num-1:line['old_num']-1]
    if line['new_num'] > cur_new_num:
      diff['new_code'] += new_code_lines[cur_new_num-1:line['new_num']-1]
    cur_old_num = line['old_num'] + 1
    cur_new_num = line['new_num'] + 1
  return json.dumps(diff)

@app.route('/save_program/', methods=['POST'])
@login_required
def save_program():
  title = request.form['title']
  code = request.form['code']
  program = None
  diff = None
  time_now = datetime.datetime.now()
  if 'program_id' in request.form:
    program = Program.query.filter_by(id=request.form['program_id'], user_id=current_user.id).first()
    prev_revision_count = CodeRevision.query.filter_by(program_id=program.id, user_id=current_user.id).count()
    prev_revision_count = 1
    if prev_revision_count > 0:
      diff = compute_diff(program.code, code)
    else:
      diff = compute_diff('', code)
    program.title = title
    program.code = code
    program.last_modified = time_now
  else:
    diff = compute_diff('', code)
    program = Program(title=title, code=code, user_id=current_user.id, last_modified=time_now)
  code_revision = CodeRevision(title=title, diff=diff, time=time_now, program_id=program.id, user_id=current_user.id)
  if 'lab_id' in request.form:
    lab_program = LabProgram.query.filter_by(lab_id=request.form['lab_id'], user_id=current_user.id).first()
    if lab_program == None:
      lab_program = LabProgram(section=request.form['section'], lab_id=request.form['lab_id'], user_id=current_user.id, program_id=program.id)
    else:
      lab_program.section = request.form['section']
      lab_program.program_id = program.id
    db.session.add(lab_program)
  db.session.add(program)
  db.session.add(code_revision)
  db.session.commit()
  return str(program.id)

@app.route('/delete_program/', methods=['POST'])
@login_required
def delete_program():
  program = Program.query.filter_by(id=request.form['program_id'], user_id=current_user.id).first()
  db.session.delete(program)
  db.session.commit()
  return ''

@app.route('/save_code_run/', methods=['POST'])
def save_code_run():
  code_run = CodeRun(title=request.form['title'], code=request.form['code'], time=datetime.datetime.now())
  if 'output' in request.form:
    code_run.output = request.form['output']
  if 'error' in request.form:
    code_run.error = request.form['error']
  if current_user.is_authenticated():
    code_run.user_id = current_user.id
  if request.form['program_id'] != '-1':
    code_run.program_id = request.form['program_id']
  db.session.add(code_run)
  db.session.commit()
  return ''

@app.route('/run_server_code/', methods=['POST'])
@roles_required('admin')
def run_server_code():
  title = request.form['title']
  code = request.form['code']
  folder_name = 'tmp_' + str(uuid.uuid4()) + '/'
  if not os.path.exists(folder_name):
    os.makedirs(folder_name)
  f = open(folder_name + title, 'w')
  f.write(code)
  f.close()
  output_name = folder_name + 'output_' + str(uuid.uuid4())
  subprocess.call('python ' + folder_name + pipes.quote(title) + ' > ' + output_name + ' 2>&1', shell=True)
  outf = open(output_name, 'r')
  output = outf.read()
  outf.close()
  shutil.rmtree(folder_name)
  return output

@app.route('/assignments/')
def assignments_home():
  assignments = Assignment.query.order_by(Assignment.deadline).all()
  return render_template('assignment_home.html', assignments=assignments)

@app.route('/assignments/<int:assignment_id>')
def assignments(assignment_id):
  assignment = Assignment.query.get(assignment_id)
  if assignment is not None:
    return render_template('assignment.html', assignment=assignment)
  else:
    return redirect('/assignments/1')

@app.route('/submit_assignment/', methods=['POST'])
@login_required
def submit_assignment():
  program = Program.query.filter_by(id=request.form['program_id'], user_id=current_user.id).first()
  submission = Submission(title=program.title, code=program.code, assignment_id=request.form['assignment_id'], user_id=current_user.id)
  db.session.add(submission)
  db.session.commit()
  return ''

@app.route('/cheatsheet.html')
def cheatsheet():
  return render_template('cheatsheet.html')

@app.route('/dashboard/')
@login_required
def user_dashboard():
  context = {}
  context['total_score'] = 0
  context['total_points'] = 0
  assignment_models = Assignment.query.order_by(Assignment.deadline).all()
  assignments = map(lambda x: x.__dict__, assignment_models)
  for assignment in assignments:
    submission = Submission.query.filter_by(assignment_id=assignment['id'], user_id=current_user.id).order_by(Submission.submit_time.desc()).first()
    if submission != None:
      assignment['submission'] = submission
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
  context['programs'] = Program.query.filter_by(user_id=current_user.id).order_by(Program.last_modified.desc()).all()


  return render_template('dashboard.html', context=context)


###############################################################################
# Admin Routes
################################################################################

@app.route('/admin/')
@roles_required('admin')
def admin_dashboard():
  student_models = User.query.filter(User.roles.any(Role.name == 'user'), User.roles.any(Role.name == 'decal'))
  user_models = User.query.filter(User.roles.any(Role.name == 'user'))
  student_set = set(student_models.all())
  nonstudent_set = set(user_models.all()) - student_set

  assignments = Assignment.query.order_by(Assignment.deadline).all()

  def templatize_data(models):
    students = map(lambda x: x.__dict__, models)
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
    return students

  students = templatize_data(student_set)
  nonstudents = templatize_data(nonstudent_set)

  return render_template('admin/dashboard.html', students=students, nonstudents=nonstudents, assignments=assignments)

@app.route('/admin/submissions/<int:submission_id>')
@roles_required('admin')
def admin_submission(submission_id):
  submission = Submission.query.filter_by(id=submission_id).first()
  if submission == None:
    return redirect('/admin/dashboard/')
  assignment = Assignment.query.filter_by(id=submission.assignment_id).first()
  user = User.query.filter_by(id=submission.user_id).first()
  return render_template('admin_submission.html', submission=submission, assignment=assignment, user=user)

@app.route('/admin/assignments/<int:assignment_id>')
@roles_required('admin')
def admin_assignment(assignment_id):
  user_models = User.query.all()
  users = map(lambda x: x.__dict__, user_models)
  assignment = Assignment.query.filter_by(id=assignment_id).first()
  for user in users:
    grade = Grade.query.filter_by(user_id=user['id'], assignment_id=assignment.id).first()
    submission = Submission.query.filter_by(user_id=user['id'], assignment_id=assignment.id).order_by(Submission.submit_time.desc()).first()
    if grade != None:
      user['grade_score'] = grade.score
    if submission != None:
      user['submission_id'] = submission.id
  return render_template('admin_assignment.html', assignment=assignment, users=users)

@app.route('/admin/submit_grade/', methods=['POST'])
@roles_required('admin')
def submit_grade():
  score = int(request.form['score'])
  assignment = Assignment.query.filter_by(id=request.form['assignment_id']).first()
  user = User.query.filter_by(id=request.form['user_id']).first()
  grade = Grade.query.filter_by(user_id=user.id, assignment_id=assignment.id).first()
  if grade == None:
    grade = Grade(assignment_id=assignment.id, user_id=user.id, score=score)
  else:
    grade.score = score
  db.session.add(grade)
  db.session.commit()
  return "success"

###############################################################################
# Public API Routes
################################################################################
@app.route('/api.public/course_info')
def show_schedule():
  weeks_sql = map(lambda x:x.__dict__, Week.query.all())
  weeks = []
  for week_obj in weeks_sql:
    week = {}
    week['assignment'] = Assignment.query.get(week_obj['assignment']).to_dict()
    week['lesson'] = Lesson.query.get(week_obj['lesson']).to_dict()
    quiz = Quiz.query.filter(Quiz.week==week_obj['id'])
    if len(quiz.all()) == 1:
      week['quiz'] = quiz.first().to_dict()
    weeks.append(week)

  data = {
      'schedule': weeks,
      'title': 'Programming: Feel the Power',
      'course': 'CS 98/198',
      'units': 2,
      'What da fox say?': 'Ring-ding-ding-ding-dingeringeding!'
      }

  return Response(response=cgi.escape(json.dumps(data)), status=200, mimetype="application/json")
