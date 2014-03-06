import os, sys, sqlite3, datetime, json, subprocess, pipes, uuid, shutil, cgi, ast, sets, dateutil.parser
from collections import defaultdict
from flask import Flask, render_template, redirect, Markup, jsonify, url_for, request, send_file, Response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import not_, and_
from sqlalchemy.sql import func
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, current_user
from flask.ext.security.signals import user_registered
from flask.ext.login import logout_user
from flask_security.forms import RegisterForm, TextField, Required

import utils
import ast_utils
import random
from types import NoneType
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
  website = db.Column(db.String(120))
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

class Assignment(db.Model):
  id = db.Column(db.Integer(), primary_key = True)
  name = db.Column(db.String(100), index = True, unique = True, nullable = False)
  semester = db.Column(db.String(100), nullable = False)
  href = db.Column(db.Text(), nullable = False)
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
  submitted = db.Column(db.DateTime(), nullable = False)
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
  deadline = db.Column(db.DateTime(), nullable=False)
  assignment_id = db.Column(db.Integer(), db.ForeignKey('assignment.id'))
  questions = db.relationship('QuizQuestion', lazy='dynamic', backref='quiz')

  def to_dict(self):
    return {
        'id': self.id,
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
    return {'id': self.id, 'question': self.question, 'answer_choices': self.answer_choices, 'solution': self.solution, 'quiz_id': self.quiz_id}

class QuizResponse(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  submit_time = db.Column(db.DateTime(), nullable=False)
  quiz_id = db.Column(db.Integer(), db.ForeignKey('quiz.id'), nullable=False)
  question_id = db.Column(db.Integer(), db.ForeignKey('quiz_question.id'), nullable=False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
  user_answer = db.Column(db.String(100), nullable=False)

templates_concepts = db.Table('templates_concepts',
    db.Column('practice_problem_template_id', db.Integer(), db.ForeignKey('practice_problem_template.id')),
    db.Column('practice_problem_concept_id', db.Integer(), db.ForeignKey('practice_problem_concept.id')))

class Homework(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  week = db.Column(db.Integer(), nullable=False)
  deadline = db.Column(db.DateTime(), nullable=False)
  assignment_id = db.Column(db.Integer(), db.ForeignKey('assignment.id'))

class HomeworkProblem(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  deadline = db.Column(db.DateTime(), nullable=False)
  homework_id = db.Column(db.Integer(), db.ForeignKey('homework.id'))
  template_id = db.Column(db.Integer(), db.ForeignKey('practice_problem_template.id'))

class Language(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  language = db.Column(db.Text(), nullable=False)

#TODO pull data from table for multiple languages
language_map = {'python':1, 1:'python', 'javascript':2, 2:'javascript'}

class PracticeProblemTemplate(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  problem_name = db.Column(db.Text(), nullable=False)
  prompt = db.Column(db.Text(), nullable=False)
  solution = db.Column(db.Text(), nullable=False)
  test = db.Column(db.Text(), nullable=False)
  hint = db.Column(db.Text(), nullable=False)
  gen_template_vars = db.Column(db.Text(), nullable=False)
  concepts = db.relationship('PracticeProblemConcept', secondary=templates_concepts,
      backref=db.backref('practice_problem_template', lazy='dynamic'), lazy='dynamic')
  is_current = db.Column(db.Boolean(), nullable=False)
  is_homework = db.Column(db.Boolean(), nullable=False)
  language_id = db.Column(db.Integer(), db.ForeignKey('language.id'), nullable=False)


  def to_dict(self):
    return {
      'id': self.id,
      'problem_name': self.problem_name,
      'prompt': self.prompt,
      'solution': self.solution,
      'test': self.test,
      'hint': self.hint,
      'gen_template_vars': self.gen_template_vars,
      'concepts': self.concepts,
      'is_current': self.is_current,
      'language_id': self.language_id
    }

submissions_concepts = db.Table('submissions_concepts',
    db.Column('practice_problem_submission_id', db.Integer(), db.ForeignKey('practice_problem_submission.id')),
    db.Column('practice_problem_concept_id', db.Integer(), db.ForeignKey('practice_problem_concept.id')))

class PracticeProblemSubmission(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  code = db.Column(db.Text(), nullable=False)
  result_test = db.Column(db.Text(), nullable=False)
  result_test_error = db.Column(db.Boolean(), nullable=False)
  result_no_test = db.Column(db.Text(), nullable=False)
  result_no_test_error = db.Column(db.Boolean(), nullable=False)
  got_hint = db.Column(db.Boolean(), nullable=False)
  gave_up = db.Column(db.Boolean(), nullable=False)
  correct = db.Column(db.Boolean(), nullable=False)
  started = db.Column(db.DateTime(), nullable=False)
  submitted = db.Column(db.DateTime(), nullable=False)
  template_vars = db.Column(db.Text(), nullable=False)
  problem_id = db.Column(db.Integer(), db.ForeignKey('practice_problem_template.id'), nullable=False)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
  language_id = db.Column(db.Integer(), db.ForeignKey('language.id'), nullable=False)
  concepts = db.relationship('PracticeProblemConcept', secondary=submissions_concepts,
      backref=db.backref('practice_problem_submission', lazy='dynamic'), lazy='dynamic')
  def to_dict(self):
    return {
      'id': self.id,
      'code': self.code,
      'result_test': self.result_test,
      'result_test_error': self.result_test_error,
      'result_no_test': self.result_no_test,
      'result_no_test_error': self.result_no_test_error,
      'got_hint': self.got_hint,
      'gave_up': self.gave_up,
      'correct': self.correct,
      'started': self.started,
      'submitted': self.submitted,
      'template_vars': self.template_vars,
      'problem_id': self.problem_id,
      'user_id': self.user_id,
      'language_id': self.language_id,
      'concepts': self.concepts
    }

class PracticeProblemConcept(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.Text(), nullable=False)
  display_name = db.Column(db.Text())
  explanation = db.Column(db.Text())
  language_id = db.Column(db.Integer(), db.ForeignKey('language.id'), nullable=False)

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
  # TODO add new schedule
  #weeks = map(lambda x:x.__dict__, Week.query.all())
  weeks = []
  # not sure if this is the best way
  for week in weeks:
    week['assignment'] = Assignment.query.get(week['assignment'])
    week['lesson'] = Lesson.query.get(week['lesson'])
    quiz = Quiz.query.filter(Quiz.week==week['id'])
    if len(quiz.all()) == 1:
      week['quiz'] = quiz.first()
  return render_template('about.html', weeks=weeks)

@app.route('/about/fa13/')
def about_fa13():
  return render_template('about_fa13.html')

@app.route('/lessons/')
def lesson_home():
  context = {}
  lessons = map(lambda x: x.__dict__, Lesson.query.all())
  context['lessons'] = lessons
  context['lesson_name'] = 'Lessons'
  return render_template('lesson_home.html', context=context)

@app.route('/lessons/<path:lesson_path>/')
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

#TODO make better
@app.route('/quiz/toaster/')
def quiz_toaster():
  return quiz(1)

@app.route('/quiz/slingshot/')
def quiz_slingshot():
  return quiz(2)

@app.route('/quiz/alpaca/')
def quiz_alpaca():
  return quiz(3)

@app.route('/quiz/freedom/')
def quiz_freedom():
  return quiz(4)

@app.route('/quiz/toaster/submit/', methods=['POST'])
@login_required
def submit_quiz_toaster():
  return submit_quiz(1)

@app.route('/quiz/slingshot/submit/', methods=['POST'])
@login_required
def submit_quiz_slingshot():
  return submit_quiz(2)

@app.route('/quiz/alpaca/submit/', methods=['POST'])
@login_required
def submit_quiz_alpaca():
  return submit_quiz(3)

@app.route('/quiz/freedom/submit/', methods=['POST'])
@login_required
def submit_quiz_freedom():
  return submit_quiz(4)

@app.route('/quiz/<int:quiz_week>/')
def quiz(quiz_week):
  if not current_user.is_authenticated():
    return render_template('message.html', message='You need to log in first')

  quizzes = Quiz.query.filter_by(week=quiz_week).all()

  if len(quizzes) < 1:
    return redirect('/')

  first_quiz = quizzes[0]
  questions = map(lambda x: x.__dict__, first_quiz.questions)

  for question in questions:
    question['answer_choices'] = json.loads(question['answer_choices'])
  first_quiz = first_quiz.__dict__
  first_quiz['questions'] = questions

  quiz_responses = QuizResponse.query.filter_by(quiz_id=first_quiz['id'], user_id=current_user.id).all()

  show_solutions = False
  if len(quiz_responses) > 0:
    show_solutions = True
    first_quiz['score'] = len(first_quiz['questions'])
    first_quiz['total'] = len(first_quiz['questions'])
    responses = {}

    for quiz_response in quiz_responses:
      responses[quiz_response.question_id] = quiz_response.user_answer

    for question in questions:
      for answer_choice in question['answer_choices']:
        if answer_choice['id'] == question['solution']:
          answer_choice['correct'] = True
        elif answer_choice['id'] == responses[question['id']]:
          answer_choice['incorrect'] = True
          first_quiz['score'] -= 1

  return render_template('quiz.html', quiz=first_quiz, show_solutions=show_solutions)

@app.route('/quiz/<int:quiz_week>/submit/', methods=['POST'])
@login_required
def submit_quiz(quiz_week):
  quiz = Quiz.query.filter_by(week=quiz_week).first()
  questions = {}
  for question in map(lambda x: x.__dict__, quiz.questions):
    questions[question['id']] = question

  if quiz == None:
    return 'Error: No quiz found with given week'
  answer_choices = request.form.getlist('selected[]')
  time_now = datetime.datetime.now()
  total = len(answer_choices)
  score = 0
  for answer_choice in answer_choices:
    question_id, answer = answer_choice.strip().split(',')
    question_id = int(question_id)
    if answer == questions[question_id]['solution']:
      score += 1
    qr = QuizResponse(quiz_id=int(quiz.id), question_id=question_id, user_id=current_user.id, user_answer=answer, submit_time=time_now)
    db.session.add(qr)

  time_now = datetime.datetime.now()
  assignments = Assignment.query.filter_by(href='/quiz/' + str(quiz_week) + '/', semester='sp14').all()
  if len(assignments) == 0:
    return 'Error: No assignment found for quiz'
  else:
    assignment = assignments[0]
    grade = Grade(score=score, submitted=time_now, user_id=current_user.id, assignment_id=assignment.id)
    db.session.add(grade)
    db.session.commit()
    return 'Submitted'

@app.route('/labs/<int:lab_id>/')
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

def get_user_progress(user_id, language_id):
  all_subs = PracticeProblemSubmission.query.filter_by(user_id=user_id, language_id=language_id).all()
  attempted_probs = {}
  for sub in all_subs:
    # Id submissions by their id as well as the time the student started working
    # on it, so we only get one score per version of a problem
    sub_id = json.dumps((sub.problem_id, sub.started.isoformat()))
    score = -float('inf')
    if sub.correct:
      if sub.got_hint:
        score = 1
      else:
        score = 2
    elif sub.gave_up:
      score = -1
    if sub_id in attempted_probs:
      # Take the maximum score a student achieved on a given problem session
      # (e.g. they get full credit for getting it right second try)
      attempted_probs[sub_id] = max(attempted_probs[sub_id], score)
    else:
      attempted_probs[sub_id] = score

  # Sort problems by submission time so we can keep a running progress total
  sorted_score_tups = sorted(attempted_probs.items(), key=lambda x: json.loads(x[0])[1])
  # Keep track of problem id as well as score achieved (we may have multiple
  # scores for the same problem if the student did multiple versions of it)
  sub_score_pairs = map(lambda x: (json.loads(x[0])[0], x[1]), sorted_score_tups)

  # Keep this dictionary around so we don't repeat problem queries
  seen_problems = {}
  # Keep a set of all problems the user got without a hint and don't repeat them
  mastered_problem_ids = []
  concept_progress = {}
  problem_id_to_time_given_up = defaultdict(list)
  score_pair = None
  for i, score_pair in enumerate(sub_score_pairs):
    # If student attempted problem but never gave up or got it right, ignore it
    if score_pair[1] == -float('inf'):
      continue
    if score_pair[0] not in seen_problems:
      seen_problems[score_pair[0]] = PracticeProblemTemplate.query.filter_by(id=score_pair[0]).first()
    problem = seen_problems[score_pair[0]]
    if score_pair[1] == 2 and score_pair[0] not in mastered_problem_ids:
      mastered_problem_ids.append(score_pair[0])
    # if the user gave up on the problem, record the index the user gave up on the problem
    if score_pair[1] == -1:
      problem_id_to_time_given_up[score_pair[0]].append(i)
    for concept in problem.concepts:
      if concept.name not in concept_progress:
        concept_progress[concept.name] = 0
      concept_progress[concept.name] += score_pair[1]
      # Keep concept_progress between 0 and 10 at all times
      concept_progress[concept.name] = max(min(concept_progress[concept.name], 10), 0)

  return (mastered_problem_ids, concept_progress, score_pair, seen_problems, problem_id_to_time_given_up, len(sub_score_pairs))


def get_next_problem(user_id, language_id):
  exempt_problem_ids, concept_progress, last_prob, seen_problems, problem_id_to_time_given_up, problems_attempted = get_user_progress(user_id, language_id)

  going_back = False
  if last_prob != None:
    # If we gave up on our last problem, possibly go back to a mastered problem
    if last_prob[1] == -1:
      going_back = True
      exempt_problem_ids = []
    # Don't repeat a problem twice in a row
    if last_prob[0] not in exempt_problem_ids:
      exempt_problem_ids.append(last_prob[0])

  # Get all current problems we haven't mastered and didn't just attempt
  all_problems = PracticeProblemTemplate.query.filter(and_(and_(not_(PracticeProblemTemplate.id.in_(exempt_problem_ids)), PracticeProblemTemplate.is_current == True)), PracticeProblemTemplate.language_id == language_id).all()

  # filter out problems that the user has repeatedly given up on
  new_all_problems = []
  for prob in all_problems:
    if prob.id in problem_id_to_time_given_up:
      # if it has been at least (3 * number given up) problems since the last time problem prob has been given up on,
      # then we can reconsider this problem for use
      if problems_attempted - problem_id_to_time_given_up[prob.id][-1] > len(problem_id_to_time_given_up[prob.id]) * 3:
        new_all_problems.append(prob)
    else:
      new_all_problems.append(prob)
  if len(new_all_problems) > 5:
    all_problems = new_all_problems

  # Give each problem a score based on how well we know each of its concepts
  problem_scores = {}
  for prob in all_problems:
    prob_score = 0
    for concept in prob.concepts:
      if concept.name in concept_progress:
        prob_score += concept_progress[concept.name]
      else:
        # Unseen concepts get a score of minus 10
        prob_score -= 10
    # Normalize score by the length of the concept list
    if prob.concepts.count() > 0:
      prob_score /= float(prob.concepts.count())
    problem_scores[prob.problem_name] = prob_score

  # Sort problems by score (high score means we've learned more of its concepts)
  sorted_prob_score_pairs = sorted(problem_scores.items(), key=lambda x: x[1], reverse=True)
  # Default to easiest problem if we've mastered all problems or if we haven't
  # done any yet
  next_prob_name = 'print'
  if len(sorted_prob_score_pairs) > 0 and sorted_prob_score_pairs[0][1] > -10:
    next_prob_name = sorted_prob_score_pairs[0][0]
    # If we're going back, randomize the next problem somewhat to prevent
    # serving the same problem every time we give up on something
    if going_back:
      max_score = sorted_prob_score_pairs[0][1]
      top_prob_names = []
      for psp in sorted_prob_score_pairs:
        if psp[0] < max_score - 1:
          break
        top_prob_names.append(psp[0])
      next_prob_name = random.choice(top_prob_names)


  return next_prob_name

@app.route('/concept/<language>/<concept_name>/')
@login_required
def concept_explanation(language, concept_name):
  if language not in language_map:
    return redirect('/practice_progress/')
  language_id = language_map[language]
  concept = PracticeProblemConcept.query.filter_by(name=concept_name, language_id=language_id).first()
  if concept == None:
    return redirect('/practice_progress/')
  return render_template('concept_explanation.html', concept=concept)

@app.route('/practice_progress/<language>')
@login_required
def practice_progress(language):
  if language not in language_map:
    return redirect('/')
  return practice_progress_by_user_id(current_user.id, language_map[language])

def practice_progress_by_user_id(user_id, language_id, admin=False):
  mastered_problem_ids, concept_progress, last_prob, seen_problems, problem_id_to_time_given_up, problems_attempted = get_user_progress(user_id, language_id)
  language = language_map[language_id]

  # Get a list of mastered problems that are still current,
  # in reverse order of mastery
  mastered_problems = []
  for prob_id in reversed(mastered_problem_ids):
    if seen_problems[prob_id].is_current:
      mastered_problems.append(seen_problems[prob_id].to_dict())

  # Get percent of current problems that have been mastered
  current_problem_count = PracticeProblemTemplate.query.filter_by(is_current=True, language_id=language_id).count()
  mastered_percent = int(float(len(mastered_problems)) / current_problem_count * 100)

  # Get progress for all concepts, including ones the user has not yet encountered
  all_concepts = PracticeProblemConcept.query.filter_by(language_id=language_id).all()
  all_concept_progress = {}
  concept_display_names = {}
  for concept in all_concepts:
    all_concept_progress[concept.name] = 0
    concept_display_names[concept.name] = concept.display_name
  for concept_name, concept_score in concept_progress.items():
    # Convert concept_score to a percentage, assuming it is out of ten
    all_concept_progress[concept_name] = float(concept_score) * 10
  sorted_concept_progress = sorted(all_concept_progress.items(), key=lambda x: x[1], reverse=True)
  # Get map of concept display names to scores
  display_concept_progress = []
  for name, score in sorted_concept_progress:
    display_concept_progress.append((name, concept_display_names[name], score))

  user = User.query.get(user_id)

  # Get all attempts
  all_attempts = PracticeProblemSubmission.query.filter_by(user_id=user_id, language_id=language_id)
  attempts = []

  current_problem_id = -1
  for att in all_attempts:
    if current_problem_id != att.problem_id:
      if current_problem_id != -1:
        attempts.append(current_attempt)
      current_problem_id = att.problem_id
      current_problem_name = PracticeProblemTemplate.query.get(att.problem_id).problem_name
      current_attempt = {'gave_up': False, 'got_hint': False, 'correct': False, 'num_attempted': 0, 'problem_name': current_problem_name}
    current_attempt['num_attempted'] += 1
    current_attempt['got_hint'] |= att.got_hint
    current_attempt['correct'] |= att.correct
    current_attempt['gave_up'] = att.gave_up
  if current_problem_id != -1:
    attempts.append(current_attempt)
  return render_template('practice_progress.html', mastered_problems=mastered_problems, mastered_percent=mastered_percent, concept_progress=display_concept_progress, name=user.firstname + ' ' + user.lastname, attempts = attempts, admin=admin, user_id=user_id, language=language)

@app.route('/practice/<language>/')
@login_required
def practice_default(language):
  if language not in language_map:
    return redirect('/')
  next_problem_name = get_next_problem(current_user.id, language_map[language])
  return redirect('/practice/%s/%s/' % (language, next_problem_name))

@app.route('/homework/')
@login_required
def homework():
  language_id = language_map['javascript'];
  problem_list = HomeworkProblem.query.order_by(HomeworkProblem.deadline).all()
  correct_subs = PracticeProblemSubmission.query.filter_by(user_id=current_user.id, language_id=language_id, correct=True).all()
  correct_ids = map(lambda x: x.problem_id, correct_subs)
  for problem in problem_list:
    if problem.template_id not in correct_ids:
      return redirect('/homework/problem/' + str(problem.id) + '/')
  return redirect('/homework/calendar/')

@app.route('/homework/calendar/')
@login_required
def homework_calendar():
  language_id = language_map['javascript'];
  day_map = {1: 'Thu', 2: 'Fri', 3: 'Sat', 4: 'Sun', 5: 'Mon', 6: 'Tue'}
  problem_list = HomeworkProblem.query.order_by(HomeworkProblem.deadline).all()
  homework_list = Homework.query.all()
  template_list = PracticeProblemTemplate.query.filter_by(language_id=language_id).all()
  template_dict = {}
  for template in template_list:
    template_dict[template.id] = template
  homework_dict = {}
  for homework in homework_list:
    homework_dict[homework.id] = homework
  correct_subs = PracticeProblemSubmission.query.filter_by(user_id=current_user.id, language_id=language_id, correct=True).all()
  correct_ids = map(lambda x: x.problem_id, correct_subs)
  homeworks = {}
  for problem in problem_list:
    template = template_dict[problem.template_id]
    homework = homework_dict[problem.homework_id]
    problem_obj = template.to_dict()
    problem_day = 6 - (homework.deadline - problem.deadline).days
    problem_obj['problem_id'] = problem.id
    problem_obj['completed'] = problem.template_id in correct_ids
    if homework.week not in homeworks:
      homeworks[homework.week] = {}
    if problem_day not in homeworks[homework.week]:
      homeworks[homework.week][problem_day] = []
    homeworks[homework.week][problem_day].append(problem_obj)
  return render_template('homework_calendar.html', homeworks=homeworks, day_map=day_map)

@app.route('/homework/problem/<int:problem_id>/')
@login_required
def homework_prob(problem_id):
  language_id = language_map['javascript']
  homework_problem = HomeworkProblem.query.filter_by(id=problem_id).first();
  if homework_problem == None:
    return redirect('/')
  problem_obj = PracticeProblemTemplate.query.get(homework_problem.template_id);
  problem = problem_obj.to_dict()
  problem['template_vars'] = utils.get_template_vars(problem['gen_template_vars'])
  problem = utils.get_problem(problem, language_id)

  # Deal with concepts
  concept_names = ast_utils.get_concepts(problem['solution'], language_id)
  problem['concept_names'] = json.dumps(concept_names)
  # Remove from our problem template any concepts which are not found in this
  # random version of it
  concepts = problem['concepts'].all()
  edited = False
  for i in range(len(concepts)-1, -1, -1):
    if concepts[i].name not in concept_names:
      del concepts[i]
      edited = True
  if edited:
    problem_obj.concepts = concepts
    db.session.commit()

  # Handle start_time server side
  dthandler = lambda obj: obj.isoformat()
  start_time = json.dumps(datetime.datetime.now(), default=dthandler)
  problem['start_time'] = start_time

  return render_template('homework.html', problem=problem, homework=homework_problem)

@app.route('/practice/<language>/<problem_name>/')
@login_required
def practice(language, problem_name):
  if not current_user.is_authenticated():
    return render_template('message.html', message='You need to log in first')
  if language not in language_map:
    return redirect('/')
  language_id = language_map[language]

  problem_obj = PracticeProblemTemplate.query.filter_by(problem_name=problem_name, is_current=True, language_id=language_id).first()

  if problem_obj is not None:
    problem = problem_obj.to_dict()
    problem['template_vars'] = utils.get_template_vars(problem['gen_template_vars'])
    problem = utils.get_problem(problem, language_id)
    concept_names = ast_utils.get_concepts(problem['solution'], language_id)
    problem['concept_names'] = json.dumps(concept_names)
    # Remove from our problem template any concepts which are not found in this
    # random version of it
    concepts = problem['concepts'].all()
    edited = False
    display_concepts = []
    for i in range(len(concepts)-1, -1, -1):
      if concepts[i].name not in concept_names:
        del concepts[i]
        edited = True
      else:
        display_concepts.append((concepts[i].name, concepts[i].display_name))
    if edited:
      problem_obj.concepts = concepts
      db.session.commit()

    # Get a list of new concepts, if there are any. This is extremely
    # inefficient because we already queried all the user's submissions to
    # figure out which problem to serve next
    all_subs = PracticeProblemSubmission.query.filter_by(user_id=current_user.id, language_id=language_id).all()
    seen_concept_names = sets.Set()
    for sub in all_subs:
      if sub.correct:
        for concept in sub.concepts.all():
          seen_concept_names.add(concept.name)
    new_concepts = []
    for concept in concepts:
      if concept.name not in seen_concept_names:
        new_concepts.append((concept.name, concept.display_name))

    # Handle start_time server side
    dthandler = lambda obj: obj.isoformat()
    start_time = json.dumps(datetime.datetime.now(), default=dthandler)
    problem['start_time'] = start_time

    return render_template('practice.html', problem=problem, concepts=display_concepts, new_concepts=new_concepts, language=language)
  else:
    return redirect('/practice/%s' % language)

@app.route('/practice_progress/<language>/<problem_name>/')
@login_required
def practice_view(language, problem_name):
  if language not in language_map:
    return redirect('/')
  return practice_view_by_user_id(current_user.id, language_map[language], problem_name)

def practice_view_by_user_id(user_id, language_id, problem_name, fullhistory=False, admin=False):
  problem_obj = PracticeProblemTemplate.query.filter_by(problem_name=problem_name, is_current=True, language_id=language_id).first()
  if problem_obj == None:
    return redirect('/practice_progress/%s' % language_map[language_id])

  if fullhistory:
    problem_submissions = PracticeProblemSubmission.query.filter_by(user_id=user_id, language_id=language_id, problem_id=problem_obj.id).order_by(PracticeProblemSubmission.submitted.desc())
    if problem_submissions == None:
      return redirect('/practice_progress/%s' % language_map[language_id])
    problem_submissions = list(problem_submissions)
    if len(problem_submissions) == 0:
      return redirect('/practice_progress/%s' % language_map[language_id])

    problem = problem_obj.to_dict()
    problem['template_vars'] = problem_submissions[0].template_vars
    problem = utils.get_problem(problem, language_id)
  else:
    problem_submission = PracticeProblemSubmission.query.filter_by(user_id=user_id, language_id=language_id, problem_id=problem_obj.id, correct=True).order_by(PracticeProblemSubmission.started.desc()).first()
    if problem_submission == None:
      return redirect('/practice_progress/%s' % language_map[language_id])

    problem = problem_obj.to_dict()
    problem['template_vars'] = problem_submission.template_vars
    problem = utils.get_problem(problem, language_id)

  if fullhistory:
    return render_template('practice_view_history.html', problem=problem, user_submissions=problem_submissions, admin=admin, user_id=user_id, language=language_map[language_id])
  else:
    return render_template('practice_view.html', problem=problem, user_solution=problem_submission.code, language=language_map[language_id])

@app.route('/admin/practice_progress/<user_id>/<language>/')
@roles_required('admin')
def admin_practice_progress(user_id, language):
  if language not in language_map:
    return redirect('/')
  return practice_progress_by_user_id(user_id, language_map[language], admin=True)

@app.route('/admin/practice_progress/<user_id>/<language>/<problem_name>/')
@roles_required('admin')
def admin_practice_view(user_id, language, problem_name):
  if language not in language_map:
    return redirect('/')
  return practice_view_by_user_id(user_id, language_map[language], problem_name, fullhistory=True, admin=True)


# Parses x for dicts, and returns a tuple where the first item is a list of the
# dicts and the second item is x with all the dicts removed
def str_remove_dicts(x):
  in_single_quotes = False
  in_double_quotes = False
  escaped = False
  dict_nest_level = 0
  dict_start_idx = 0
  i = 0
  dicts = []
  while i < len(x):
    ch = x[i]
    if ch == "'" and not escaped and not in_double_quotes:
      in_single_quotes = not in_single_quotes
    if ch == '"' and not escaped and not in_single_quotes:
      in_double_quotes = not in_double_quotes
    if ch == "\\":
      escaped = not escaped
    else:
      escaped = False
    if ch == '{' and not in_single_quotes and not in_double_quotes:
      if dict_nest_level == 0:
        dict_start_idx = i
      dict_nest_level += 1
    if ch == '}' and not in_single_quotes and not in_double_quotes:
      dict_nest_level -= 1
      if dict_nest_level == 0:
        dicts.append(ast.literal_eval(x[dict_start_idx:i+1]))
        x = x[:dict_start_idx] + x[i+1:]
        i = dict_start_idx - 1
    i += 1
  return (dicts, x)

# Check if two dicts are the same, ignoring key order
def same_dict(x, y):
  if len(x.keys()) != len(y.keys()):
    return False
  for k, v in x.items():
    if y[k] != v:
      return False
  return True

# Check if two output strings are really the same
# Ignores dictionary print order
def same_output(x, y):
  x_dicts, x_code = str_remove_dicts(x)
  y_dicts, y_code = str_remove_dicts(y)
  if x_code.strip() != y_code.strip():
    return False
  if len(x_dicts) != len(y_dicts):
    return False
  for i, d in enumerate(x_dicts):
    if not same_dict(y_dicts[i], d):
      return False
  return True

@app.route('/practice/<language>/<problem_name>/submit/', methods=['POST'])
@login_required
def submit_practice(language, problem_name):
  if language not in language_map:
    return 'error'
  language_id = language_map[language]
  code = request.form['code']
  result_test = request.form['result_test']
  result_no_test = request.form['result_no_test']
  result_test_error = 1 if request.form['result_test_error'] == 'true' else 0
  result_no_test_error = 1 if request.form['result_no_test_error'] == 'true' else 0
  start_time = dateutil.parser.parse(json.loads(request.form['start_time']))
  submit_time = datetime.datetime.now()
  template_vars = request.form['template_vars']
  concept_names = json.loads(request.form['concept_names'])
  concepts = []
  for concept_name in concept_names:
    concept = PracticeProblemConcept.query.filter_by(name=concept_name, language_id=language_id).first()
    if concept == None:
      concept = PracticeProblemConcept(name=concept_name, language_id=language_id)
      db.session.add(concept)
      db.session.commit()
    concepts.append(concept)
  problem = PracticeProblemTemplate.query.filter_by(problem_name=problem_name, is_current=True, language_id=language_id).first().to_dict()
  got_hint = True if request.form['got_hint'] == 'true' else False
  gave_up = True if request.form['gave_up'] == 'true' else False
  problem['template_vars'] = template_vars
  problem = utils.get_problem(problem, language_id)
  correct = same_output(problem['expected_test'], result_test) and same_output(problem['expected_no_test'], result_no_test)
  submission = PracticeProblemSubmission(problem_id=problem['id'], language_id=language_id, user_id=current_user.id, code=code, result_test=result_test, result_no_test=result_no_test, result_test_error=result_test_error, result_no_test_error=result_no_test_error, got_hint=got_hint, gave_up=gave_up, correct=correct, started=start_time, submitted=submit_time, template_vars=problem['template_vars'], concepts=concepts)
  db.session.add(submission)
  db.session.commit()
  return_data = {}
  if correct:
    return_data['correct'] = 'correct'
    return_data['solution'] = problem['solution']
  elif result_no_test_error:
    return_data['correct'] = 'error'
  else:
    # Insert random inspirational failure quote
    return_data['correct'] = 'incorrect'
    failure_quotes = [
        ('Our greatest glory is not in never failing, but in rising up every time we fail.', 'Ralph Waldo Emerson'),
        ('Satisfaction lies in the effort, not in the attainment. Full effort is full victory.', 'Mahatma Gandhi'),
        ('As you proceed through life, following your own path, birds will shit on you. Don\'t bother to brush it off. Getting a comedic view of your situation gives you spiritual distance. Having a sense of humor saves you.', 'Joseph Campbell'),
        ('If you focus on the risks, they\'ll multiply in your mind and eventually paralyze you. You want to focus on the task, instead, on doing what needs to be done.', 'Barry Eisler'),
        ('If you take responsibility and blame yourself, you have the power to change things. But if you put responsibility on someone else, then you are giving them the power to decide your fate.', 'Deja King'),
        ('H is for Habit, winners make a habit of doing the things losers don\'t want to do.', 'Lucas Remmerswaal'),
        ('Success is a state of mind.  If you want success, start thinking of yourself as a success.', 'Joyce Brothers'),
        ("If you set your goals ridiculously high and it's a failure, you will fail above everyone elses success", 'James Cameron'),
        ('Genius is one percent inspiration and ninety-nine percent perspiration.', 'Thomas Edison'),
        ('Luck is the dividend of sweat. The more you sweat, the luckier you get.', 'Ray Kroc'),
        ('To have failed is to have striven, to have striven is to have grown.', 'Maltbie Davenport Babcock'),
        ('He who does not hope to win has already lost.', 'Jose Joaquin Olmedo'),
        ('When you get crapped on, grow a garden.', 'Tanja Kobasic'),
        ('It is the work that matters, not the applause that follows.', 'Robert Falco Scott'),
        ("I have not failed. I've just found 10,000 ways that won't work.", 'Thomas Edison'),
        ('Success is not final, failure is not fatal: it is the courage to continue that counts.', 'Winston Churchill'),
        ('Pain is temporary. Quitting lasts forever.', 'Lance Armstrong'),
        ('Failure is the condiment that gives success its flavor.', 'Truman Capote'),
        ('Success is stumbling from failure to failure with no loss of enthusiasm.', 'Winston Churchill'),
        ("The brick walls are there for a reason. The brick walls are not there to keep us out. The brick walls are there to give us a chance to show how badly we want something. Because the brick walls are there to stop the people who don't want it badly enough. They're there to stop the other people.", 'Randy Pausch'),
        ("A thinker sees his own actions as experiments and questions--as attempts to find out something. Success and failure are for him answers above all.", 'Friedrich Nietzsche'),
        ("A bad day for your ego is a great day for your soul.", 'Jillian Michaels'),
        ('Never confuse a single defeat with a final defeat.', 'F. Scott Fitzgerald'),
        ("You're not obligated to win. You're obligated to keep trying. To the best you can do everyday.", 'Jason Mraz'),
        ('If you fell down yesterday, stand up today.', 'H.G. Wells'),
        ('We are all failures- at least the best of us are.', 'J.M. Barrie'),
        ('Try again. Fail again. Fail better.', 'Samuel Beckett'),
        ('The only real mistake is the one from which we learn nothing.', 'Henry Ford'),
        ('Failures are finger posts on the road to achievement.', 'C.S. Lewis'),
        ('The person who failed often knows how to avoid future failures. The person who knows only success can be more oblivious to all the pitfalls.', 'Randy Pausch'),
        ('As long as I am breathing, in my eyes, I am just beginning.', 'Criss Jami'),
        ('The harder you fall, the heavier your heart; the heavier your heart, the stronger you climb; the stronger you climb, the higher your pedestal.', 'Criss Jami'),
        ("All the time you're saying to yourself, \"I could do that, but I won't,\"--which is just another way of saying that you can't.", "Richard P. Feynman"),
        ("All men make mistakes, but a good man yields when he knows his course is wrong, and repairs the evil. The only crime is pride.", 'Sophocles'),
        ("Winners are not afraid of losing. But losers are. Failure is part of the process of success. People who avoid failure also avoid success.", 'Robert T. Kiyosaki'),
        ("What seems to us as bitter trials are often blessings in disguise", 'Oscar Wilde'),
        ("Failure should be our teacher, not our undertaker. Failure is delay, not defeat. It is a temporary detour, not a dead end. Failure is something we can avoid only by saying nothing, doing nothing, and being nothing.", 'Denis Waitley'),
        ("'Almost' only counts in horseshoes and hand grenades.", 'Anonymous'),
        ("You build on failure. You use it as a stepping sone. Close the door on the past. You don't try to forget the mistakes, but you don't dwell on it. You don't let it have any of your energy, or any of your time, or any of your space.", 'Johnny Cash'),
        ("We have forty million reasons for failure, but not a single excuse.", 'Rudyard Kipling'),
        ("Failure? I never encountered it. All I ever met were temporary setbacks.", 'Dottie Walters'),
        ("The major difference between a thing that might go wrong and a thing that cannot possibly go wrong is that when a thing that cannot possibly go wrong goes wrong it usually turns out to be impossible to get at or repair.", 'Douglas Adams'),
        ('A man who fails well is greater than one who succeeds badly.', 'Thomas Merton'),
        ('Our business in this world is not to succeed, but to continue to fail, in good spirits.', 'Robert Louis Stevenson'),
        ("If at first you don't succeed, try, try, try again.", 'Anonymous')
        ]
    return_data['failure_quote'] = random.choice(failure_quotes)
  return json.dumps(return_data)

@app.route('/workspace/')
def workspace_home():
  if current_user.is_authenticated():
    programs = Program.query.filter_by(user_id=current_user.id).order_by(Program.last_modified.desc()).all()
    return render_template('workspace_home.html', programs=programs)
  return render_template('workspace.html')

@app.route('/workspace/<int:program_id>/')
@login_required
def workspace(program_id):
  program = Program.query.filter_by(id=program_id, user_id=current_user.id).first()
  if program == None:
    return redirect('/workspace/')
  return render_template('workspace.html', program=program)

@app.route('/workspace/<int:program_id>/revision/<int:revision_id>/')
@login_required
def program_revision(program_id, revision_id):
  program = Program.query.filter_by(id=program_id, user_id=current_user.id).first()
  if program == None:
    return redirect('/workspace/')
  target_revision = CodeRevision.query.filter_by(id=revision_id, program_id=program.id, user_id=current_user.id).first()
  if target_revision == None:
    return redirect('/workspace/%s/' % str(program.id))
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
  return redirect('/workspace/%s/' % str(program.id))

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

@app.route('/assignments/<int:assignment_id>/')
def assignments(assignment_id):
  assignment = Assignment.query.get(assignment_id)
  if assignment is not None:
    return render_template('assignment.html', assignment=assignment)
  else:
    return redirect('/assignments/1/')

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

@app.route('/jscheatsheet.html')
def jscheatsheet():
  return render_template('jscheatsheet.html')

@app.route('/html_cheatsheet.html')
def html_cheatsheet():
  return render_template('html_cheatsheet.html')

def calc_homework_grades(user_id):
  language_id = language_map['javascript']
  homeworks = Homework.query.all()
  homework_dict = {}
  for homework in homeworks:
    homework_dict[homework.id] = 0
  homework_problems = HomeworkProblem.query.all()
  correct_subs = PracticeProblemSubmission.query.filter_by(user_id=user_id, language_id=language_id, correct=True).all()
  correct_dict = {}
  for sub in correct_subs:
    correct_dict[sub.problem_id] = sub
  for problem in homework_problems:
    # Deal with UTC / PST time delta and daylight savings
    tz_delta = datetime.timedelta(hours=8)
    if problem.deadline >= datetime.datetime(2014, 3, 9, 2, 0, 0):
      tz_delta = datetime.timedelta(hours=7)
    for template_id, sub in correct_dict.iteritems():
      if problem.template_id == template_id and sub.submitted <= problem.deadline + tz_delta:
        homework_dict[problem.homework_id] += 1
        break
  for homework in homeworks:
    grade = Grade.query.filter_by(assignment_id=homework.assignment_id, user_id=user_id).first()
    time_now = datetime.datetime.now()
    if grade == None:
      grade = Grade(score=homework_dict[homework.id], submitted=time_now, user_id=user_id, assignment_id=homework.assignment_id)
    else:
      grade.score = homework_dict[homework.id]
      grade.submitted=time_now
    db.session.add(grade)
    db.session.commit()

@app.route('/dashboard/')
@login_required
def user_dashboard():
  calc_homework_grades(current_user.id)
  context = {}
  context['total_score'] = 0
  context['total_points'] = 0
  assignment_models = Assignment.query.order_by(Assignment.deadline).filter_by(semester='sp14').all()
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

  # Prevent divide by zero
  if context['total_points'] == 0 and context['total_score'] == 0:
    context['total_points'] = 1

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

  assignments = Assignment.query.filter_by(semester='sp14').order_by(Assignment.deadline).all()

  def templatize_data(models):
    students = map(lambda x: x.__dict__, models)
    students = sorted(students, key=lambda x: x['id'])
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
      #TODO show breakdown of attempts per language
      student['num_practice_attempted'] = len(PracticeProblemSubmission.query.filter_by(user_id=student['id']).all())
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
    time_now = datetime.datetime.now()
    grade = Grade(assignment_id=assignment.id, submitted=time_now, user_id=user.id, score=score)
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
