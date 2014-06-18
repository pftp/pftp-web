import os
import code
import json
import sqlite3
import markdown
import time
import grequests
from markdown.postprocessors import Postprocessor
from termcolor import colored
from random import randrange, random
from datetime import datetime, timedelta
from time import strftime


from fabric.api import local, task, settings
from fabric.operations import get, put

from application import app, db, user_datastore, Role, User, Assignment, Grade, Lesson, Sublesson, Week, Quiz, QuizQuestion, PracticeProblemTemplate, PracticeProblemConcept, Language, get_next_problem, Quiz, Homework, HomeworkProblem, QuizResponse, calc_homework_grades
import utils, ast_utils
from emailer import Emailer

################################################################################
# Tasks
################################################################################

@task
def clean():
  with settings(warn_only=True):
    local('rm -rf templates/gen')
    local('rm -rf static/labs')
    local('rm pftp.db')

@task
def addpractice():
  #TODO detect languages automatically
  add_practice_problems("python")
  add_practice_problems("javascript")
  addconcepts()

@task
def addconcepts():
  add_concepts("python")
  add_concepts("javascript")

@task
def adddecalrole():
  add_decal_role()

@task
def genlabs():
  generate_labs()

@task
def emailproblems():
  email_problems()

@task
def build():
  clean()
  generate_pages()
  generate_labs()
  db.create_all()
  generate_models()
  addpractice()

#XXX make this detect changes and automatically build
@task
def console():
  context = locals()
  context['app'] = app
  context['db'] = db
  context['user_datastore'] = user_datastore
  context['Role'] = Role
  context['User'] = User
  context['Assignment'] = Assignment
  context['Grade'] = Grade
  context['Quiz'] = Quiz
  code.interact(local=locals())

@task
def pulldb():
  get('pftp/pftp.db', 'pftp.db')

@task
def pushdb():
  put('pftp.db', 'pftp/pftp.db')

@task
def backup():
  #disable pftp vhost
  local('rm /etc/apache2/sites-enabled/pftp')
  #enable mod_rewrite
  local('a2enmod rewrite')
  #enable pftp-maintenance vhost
  local('ln -s /etc/apache2/sites-available/pftp-maintenance /etc/apache2/sites-enabled/pftp-maintenance')
  #restart apache
  local('service apache2 restart')

  #db is safe, now perform backup
  local('cp pftp.db backups/%s.db' % strftime('%Y-%m-%d_%H:%M:%S'))
  #limit number of backups
  local('bash backups/clean_backups.sh')

  #disable pftp-maintenance vhost
  local('rm /etc/apache2/sites-enabled/pftp-maintenance')
  #disable mod_rewrite
  local('a2dismod rewrite')
  # enable pftp vhost
  local('ln -s /etc/apache2/sites-available/pftp /etc/apache2/sites-enabled/pftp')
  #restart apache
  local('service apache2 restart')

  #HACKHACK
  #app isn't initialized properly unless apachectl is used
  #TODO figure out why
  time.sleep(2)
  local('apachectl -k stop')
  time.sleep(2)
  local('apachectl -k start')

@task(default=True)
def run():
  app.run()

############### DeCal specific tasks #################
#TODO send concurrent HEAD requests
@task
def wake_sites():
  rs = []
  for user in User.query.filter(User.roles.any(Role.name == 'user'), User.roles.any(Role.name == 'decal')):
    if user.website:
      rs.append(grequests.head(user.website))
      print colored('Waking %s' % user.website, 'yellow')
  grequests.map(rs)
  print colored("%d sites awoken!" % len(rs), 'green')

############### Assignments Spring 2014 ###############

@task
def add_quiz0_assignment():
  quiz0 = Quiz.query.filter_by(week=0).first()
  num_questions = QuizQuestion.query.filter_by(quiz_id=quiz0.id).count()
  assignment0 = Assignment(name="Quiz 0", semester="sp14", href="/quiz/0/", description="", deadline=quiz0.deadline, points=num_questions)
  db.session.add(assignment0)
  db.session.commit()
  quiz0.assignment_id = assignment0.id
  db.session.add(quiz0)
  db.session.commit()
  print colored('quiz 0 assignment added to database', "green")

@task
def add_lab1_assignment():
  assignment = Assignment(name="Lab 1", semester="sp14", href="https://docs.google.com/document/d/1RA0P097KZLwZp_zAB63HOQVCcE5z8W6p9osu3HjGjww/pub", description="", deadline=datetime(2014,2,19,17,59), points=5)
  db.session.add(assignment)
  db.session.commit()
  print colored('lab 1 assignment added to database', "green")

@task
def add_quiz1_assignment():
  quiz1 = Quiz.query.filter_by(week=1).first()
  num_questions = QuizQuestion.query.filter_by(quiz_id=quiz1.id).count()
  assignment1 = Assignment(name="Quiz 1", semester="sp14", href="/quiz/1/", description="", deadline=quiz1.deadline, points=num_questions)
  db.session.add(assignment1)
  db.session.commit()
  quiz1.assignment_id = assignment1.id
  db.session.add(quiz1)
  db.session.commit()
  print colored('quiz 1 assignment added to database', "green")

@task
def add_homework1():
  assignment = Assignment(name="Homework 1", semester="sp14", href="/homework/calendar/", description="", deadline=datetime(2014,3,4,23,59), points=10)
  db.session.add(assignment)
  db.session.commit()
  homework1 = Homework(week=4, deadline=assignment.deadline, assignment_id=assignment.id)
  db.session.add(homework1)
  db.session.commit()
  print colored('homework 1 and assignment added to database', "green")

@task
def add_homework2():
  assignment = Assignment(name="Homework 2", semester="sp14", href="/homework/calendar/", description="", deadline=datetime(2014,3,11,23,59), points=6)
  db.session.add(assignment)
  db.session.commit()
  homework2 = Homework(week=5, deadline=assignment.deadline, assignment_id=assignment.id)
  db.session.add(homework2)
  db.session.commit()
  print colored('homework 2 and assignment added to database', "green")

@task
def add_homework3():
  assignment = Assignment(name="Homework 3", semester="sp14", href="/homework/calendar/", description="", deadline=datetime(2014,3,18,23,59), points=8)
  db.session.add(assignment)
  db.session.commit()
  homework3 = Homework(week=6, deadline=assignment.deadline, assignment_id=assignment.id)
  db.session.add(homework3)
  db.session.commit()
  print colored('homework 3 and assignment added to database', "green")

@task
def add_homework4():
  assignment = Assignment(name="Homework 4", semester="sp14", href="/homework/calendar/", description="", deadline=datetime(2014,4,9,23,59), points=8)
  db.session.add(assignment)
  db.session.commit()
  homework4 = Homework(week=7, deadline=assignment.deadline, assignment_id=assignment.id)
  db.session.add(homework4)
  db.session.commit()
  print colored('homework 4 and assignment added to database', "green")

############### Quizzes Spring 2014 ###############

@task
def add_quiz0():
  quiz0 = Quiz(name="Info Session Quiz", week=0, deadline=datetime(2014,2,5,18,59))

  question1 = QuizQuestion(question="Did you fill out <a target=\"_blank\" href=\"https://docs.google.com/forms/d/1eLxIhIyO3fhanXlbFwBI-SCNf0xBclBqdLZkrtn-sRE/viewform\">our online application</a>?",
      answer_choices=json.dumps([{'id': 'A', 'answer': 'Yes'}]), solution='A', quiz=quiz0.id)
  question2 = QuizQuestion(question="Did you register for our site with the same email address as on the application?",
      answer_choices=json.dumps([{'id': 'A', 'answer': 'Yes'}]), solution='A', quiz=quiz0.id)

  quiz0.questions.append(question1)
  quiz0.questions.append(question2)
  db.session.add(quiz0)
  db.session.add(question1)
  db.session.add(question2)
  db.session.commit()
  print colored('quiz 0 added to database', "green")

@task
def add_quiz1():
  quiz1 = Quiz(name="Week 1 Quiz", week=1, deadline=datetime(2014,2,12,18,59))

  question1 = QuizQuestion(question="In this class, you will learn",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'Python'}
          , {'id': 'B', 'answer': 'how to build Snapchat'}
          , {'id': 'C', 'answer': 'Javascript'}
          , {'id': 'D', 'answer': 'how to hack things'}
          ])
      , solution='C', quiz=quiz1.id)

  question2 = QuizQuestion(question="Which of the following is a type of value?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'Unicorns'}
          , {'id': 'B', 'answer': 'Type 0'}
          , {'id': 'C', 'answer': 'None'}
          , {'id': 'D', 'answer': 'Boolean'}
          ])
      , solution='D', quiz=quiz1.id)

  question3 = QuizQuestion(question="Javascript is the successor to Java, a popular programming language.",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'True'}
          , {'id': 'B', 'answer': 'False'}
          ])
      , solution='B', quiz=quiz1.id)

  quiz1.questions.append(question1)
  quiz1.questions.append(question2)
  quiz1.questions.append(question3)
  db.session.add(quiz1)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.commit()
  print colored('quiz 1 added to database', "green")

@task
def add_quiz2():
  assignment = Assignment(name="Quiz 2", semester="sp14", href="/quiz/2/", description="", deadline=datetime(2014,2,19,18,59), points=4)
  db.session.add(assignment)
  db.session.commit()

  quiz2 = Quiz(name="Week 2 Quiz", week=2, deadline=assignment.deadline, assignment_id=assignment.id)

  question1 = QuizQuestion(question="How does the reading tell you to imagine variables?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'As renamed values'}
          , {'id': 'B', 'answer': 'As tentacles to grasp values'}
          , {'id': 'C', 'answer': 'As boxes to contain values'}
          , {'id': 'D', 'answer': 'As envelopes to send values'}
          ])
      , solution='B')

  question2 = QuizQuestion(question="Which of the following is an example of calling a function?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'alert("Star Slinger!")'}
          , {'id': 'B', 'answer': 'var x = 5'}
          , {'id': 'C', 'answer': 'var f = function() { }'}
          , {'id': 'D', 'answer': 'All of the above'}
          ])
      , solution='A')

  question3 = QuizQuestion(question="What symbol goes at the end of every statement in JavaScript?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'Dollar Sign ($)'}
          , {'id': 'B', 'answer': 'Tilde (~)'}
          , {'id': 'C', 'answer': 'Equals sign (=)'}
          , {'id': 'D', 'answer': 'Semicolon (;)'}
          ])
      , solution='D')

  question4 = QuizQuestion(question="How do we print 'Hello World!' in JavaScript?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'console.log("Hello World!")'}
          , {'id': 'B', 'answer': 'System.out.println("Hello World!")'}
          , {'id': 'C', 'answer': 'cout << "Hello World!" << endl'}
          , {'id': 'D', 'answer': "print 'Hello World!'"}
          ])
      , solution='A')

  quiz2.questions.append(question1)
  quiz2.questions.append(question2)
  quiz2.questions.append(question3)
  quiz2.questions.append(question4)
  db.session.add(quiz2)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.add(question4)
  db.session.commit()
  print colored('quiz 2 added to database', "green")


@task
def add_quiz3():
  assignment = Assignment(name="Quiz 3", semester="sp14", href="/quiz/3/", description="", deadline=datetime(2014,2,26,18,59), points=3)
  db.session.add(assignment)
  db.session.commit()

  quiz3 = Quiz(name="Week 3 Quiz", week=3, deadline=assignment.deadline, assignment_id=assignment.id)

  question1 = QuizQuestion(question="Which of the following cannot be used to control program execution flow?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'if statements'}
          , {'id': 'B', 'answer': 'console.log statements'}
          , {'id': 'C', 'answer': 'for loops'}
          , {'id': 'D', 'answer': 'while loops'}
          ])
      , solution='B')

  question2 = QuizQuestion(question="Which of the following variables is named using 'camel case' capitalization?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'fuzzylittleturtles'}
          , {'id': 'B', 'answer': 'fuzzyLittleTurtles'}
          , {'id': 'C', 'answer': 'FuzzyLittleTurtles'}
          , {'id': 'D', 'answer': 'fuzzy_little_turtles'}
          ])
      , solution='B')

  question3 = QuizQuestion(question="What does the following code print? 'console.log(\"This is\" + 7 + \"words in a sentence.\");",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'This is + 7 + words in a sentence.'}
          , {'id': 'B', 'answer': 'This is7words in a sentence.'}
          , {'id': 'C', 'answer': 'This is 7 words in a sentence.'}
          , {'id': 'D', 'answer': '\"This is \" + 7 + \" words in a sentence.\"'}
          ])
      , solution='B')

  quiz3.questions.append(question1)
  quiz3.questions.append(question2)
  quiz3.questions.append(question3)
  db.session.add(quiz3)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.commit()
  print colored('quiz 3 added to database', "green")

@task
def add_quiz4():
  assignment = Assignment(name="Quiz 4", semester="sp14", href="/quiz/4/", description="", deadline=datetime(2014,3,5,18,59), points=3)
  db.session.add(assignment)
  db.session.commit()

  quiz4 = Quiz(name="Week 4 Quiz", week=4, deadline=assignment.deadline, assignment_id=assignment.id)

  question1 = QuizQuestion(question="Consider the following function definition:<br><br>var window = function(sill, pane) {<br>&nbsp;&nbsp;return sill * sill + pane;<br>};<br><br>What is the name of the function?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'window'}
          , {'id': 'B', 'answer': 'sill'}
          , {'id': 'C', 'answer': 'pane'}
          , {'id': 'D', 'answer': 'anonymous'}
          ])
      , solution='A')

  question2 = QuizQuestion(question="What are the parameters (also called arguments) of the above function?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'window'}
          , {'id': 'B', 'answer': 'sill and pane'}
          , {'id': 'C', 'answer': 'window, sill, and pane'}
          , {'id': 'D', 'answer': 'return'}
          ])
      , solution='B')

  question3 = QuizQuestion(question="Which of the following would print '23'?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'window(23);'}
          , {'id': 'B', 'answer': 'window(4, 7);'}
          , {'id': 'C', 'answer': 'window();'}
          , {'id': 'D', 'answer': 'console.log(window(1, 1) + "3");'}
          ])
      , solution='D')

  quiz4.questions.append(question1)
  quiz4.questions.append(question2)
  quiz4.questions.append(question3)
  db.session.add(quiz4)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.commit()
  print colored('quiz 4 added to database', "green")


@task
def add_quiz5():
  assignment = Assignment(name="Quiz 5", semester="sp14", href="/quiz/5/", description="", deadline=datetime(2014,3,12,18,59), points=3)
  db.session.add(assignment)
  db.session.commit()

  quiz5 = Quiz(name="Week 5 Quiz", week=5, deadline=assignment.deadline, assignment_id=assignment.id)

  question1 = QuizQuestion(question="Consider the following function definition:<br><br>var hotdogs = function(num) {<br>&nbsp;&nbsp;for (var i = 0; i <= num; i++) {<br>&nbsp;&nbsp;&nbsp;&nbsp;console.log(i);<br>&nbsp;&nbsp}<br>};<br><br>What does the following code print?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'Nothing gets printed because the function is never called'}
          , {'id': 'B', 'answer': 'Every number from 0 to num'}
          , {'id': 'C', 'answer': '0 1 2 3 4 5 6'}
          , {'id': 'D', 'answer': '0'}
          ])
      , solution='A')

  question2 = QuizQuestion(question="Consider the following function definition:<br><br>var hotdogs = function(num) {<br>&nbsp;&nbsp;for (var i = 0; i <= num; i++) {<br>&nbsp;&nbsp;&nbsp;&nbsp;console.log(i);<br>&nbsp;&nbsp}<br>};<br>hotdogs(10);<br><br>What does the following code print?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'Nothing gets printed because the function is never called'}
          , {'id': 'B', 'answer': '0 1 2 3 4 5 6 7 8 9 10'}
          , {'id': 'C', 'answer': '0 1 2 3 4 5 6 7 8 9'}
          ])
      , solution='B')

  question3 = QuizQuestion(question="Consider the following function definition:<br><br>var hotdogs = function(num) {<br>&nbsp;&nbsp;for (var i = 0; i <= num; i++) {<br>&nbsp;&nbsp;&nbsp;&nbsp;console.log(i);<br>&nbsp;&nbsp}<br>&nbsp;&nbsp;return num;<br>};<br>var x = hotdogs(3);<br>var y = hotdogs(4);<br>console.log(x + y);<br>What does the following code print?",
      answer_choices=json.dumps(
          [ {'id': 'A', 'answer': 'Nothing gets printed because the function is never called'}
          , {'id': 'B', 'answer': '0 1 2 3 0 1 2 3 4'}
          , {'id': 'C', 'answer': '7'}
          , {'id': 'D', 'answer': '0 1 2 3 0 1 2 3 4 7'}
          ])
      , solution='D')

  quiz5.questions.append(question1)
  quiz5.questions.append(question2)
  quiz5.questions.append(question3)
  db.session.add(quiz5)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.commit()
  print colored('quiz 5 added to database', "green")

@task
def grade_homework():
  students = User.query.filter(User.roles.any(Role.name == 'user'), User.roles.any(Role.name == 'decal'))
  count = 0
  for student in students:
    count += 1
    calc_homework_grades(student.id)
    print colored('Homework grades calculated for %s %s' % (student.firstname, student.lastname), 'yellow')
  print colored('Homework grades calculated for %d students' % count, 'green')

@task
def grade_quizzes():
  time_now = datetime.now()
  quizzes = Quiz.query.all()
  for user in User.query.filter(User.roles.any(Role.name == 'user'), User.roles.any(Role.name == 'decal')):
    for quiz in quizzes:
      grade = Grade.query.filter_by(user_id=user.id, assignment_id=quiz.assignment_id).first()
      if not grade:
        assignment = Assignment.query.filter_by(id=quiz.assignment_id).first()
        score = 0
        quiz_responses = QuizResponse.query.filter_by(user_id=user.id, quiz_id=quiz.id).all()
        responses = {}
        for quiz_response in quiz_responses:
          responses[quiz_response.question_id] = quiz_response
        if len(responses) != 0:
          for question in quiz.questions.all():
            if question.solution == responses[question.id].user_answer:
              score += 1

        grade = Grade(score=score, submitted=time_now, user_id=user.id, assignment_id=assignment.id)
        db.session.add(grade)
        print 'Added', user.email, assignment.href, str(score) + '/' + str(assignment.points)
  db.session.commit()


################################################################################
# Helpers
################################################################################
def clean_filename(filename):
  # makes it so we can order files in a directory
  if filename[0].isdigit():
    filename = filename[1:]
  return filename

def humanize(filename):
  filename = clean_filename(filename)
  uncapitalized = ['a', 'an', 'and', 'at', 'by', 'from', 'of', 'on', 'or', 'the', 'to', 'with', 'without']
  name = os.path.splitext(filename)[0]
  words = [word[0].upper() + word[1:] if word not in uncapitalized else word for word in name.split('_')]
  title = ' '.join(words)
  title = title[0].upper() + title[1:]
  return title


def generate_pages():
  markdown_template_file = open('templates/markdown_template.html', 'r')
  markdown_template = markdown_template_file.read()

  processor = markdown.Markdown()
  count = 0


  for root, subFolders, files in os.walk('markdown'):
    for filename in files:
      input_path = os.path.join(root, filename)
      output_dir = root.replace('markdown', 'templates/gen', 1)
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      input_file = open(input_path, 'r')

      if '.pdf' in filename:
        output_path = os.path.join(output_dir, filename)
        input_text = input_file.read()
        output_file = open(output_path, 'w')
        output_file.write(input_text)
        output_file.close()
        continue

      output_path = os.path.splitext(os.path.join(output_dir, filename))[0] + '.html'
      input_text = input_file.read()
      output_file = open(output_path, 'w')

      html_output = processor.convert(input_text)

      output_text = markdown_template.replace('[title]', humanize(filename)).replace('[content]', html_output)
      output_file.write(output_text)

      processor.reset()
      count += 1

  print colored("%s files generated" % count, "green")


def generate_models():
  python = Language(language="python")
  javascript = Language(language="javascript")

  db.session.add(python)
  db.session.add(javascript)

  print colored("2 languages added to database.", "green")

  user_role = user_datastore.create_role(name="user")
  admin_role = user_datastore.create_role(name="admin")

  admin_user = user_datastore.create_user(email="admin@cramm.it", firstname="Cramm", lastname="It", password="p@ssw0rd")
  user_datastore.add_role_to_user(admin_user, admin_role)

  test_user1 = user_datastore.create_user(email="test@cramm.it", firstname="Test", lastname="User", password="p@ssw0rd")
  test_user2 = user_datastore.create_user(email="test2@cramm.it", firstname="Test2", lastname="User2", password="p@ssw0rd")

  user_datastore.add_role_to_user(test_user1, user_role)
  user_datastore.add_role_to_user(test_user2, user_role)

  db.session.add(admin_user)
  db.session.add(test_user1)
  db.session.add(test_user2)

  print colored("3 users added to database.", "green")

  #assignment1 = Assignment(name='Homework 1', description='Draw something using at least 3 shapes and 3 colors. Have fun with it!',  points=5, deadline=datetime(2013,9,15,23,59))
  #assignment2 = Assignment(name='Homework 2', description='Create a turtle chatbot that can <ul><li>Understand a conversation with at least 3 levels of questions</li><li>Uses a number from raw_input (using the int() conversion)</li><li>Draw something when asked to draw (you can use your Homework 1 submission here!) with something new you learned about turtle graphics from the lab (turtle.write, turtle.circle, etc)</li></ul>', points=5, deadline=datetime(2013,9,22,23,59))
  #assignment3 = Assignment(name='Homework 3', description="Draw a scene using at least 3 nested function calls. It should be something that you wouldn't want to try drawing line by line!", points=5, deadline=datetime(2013,9,29,23,59))
  #assignment3 = Assignment(name='Project 1', description='Build a turtle graphics game', points=30, deadline=datetime(2013,10,1))
  #assignment4 = Assignment(name='Homework 3', description='Finish exercises 11-15 before next class',  points=10, deadline=datetime(2013,10,8))
  #assignment5 = Assignment(name='Homework 4', description='Finish exercises 16-20 before next class', points=10, deadline=datetime(2013,10,15))
  #assignment6 = Assignment(name='Project 2', description='Build a Flask app', points=30, deadline=datetime(2013,10,29))
  #assignment7 = Assignment(name='Homework 5', description='Finish exercises 21-25 before next class',  points=10, deadline=datetime(2013,11,5))
  #assignment8 = Assignment(name='Homework 6', description='Finish exercises 26-30 before next class', points=10, deadline=datetime(2013,11,12))
  #assignment9 = Assignment(name='Final Project', description='Build something cool', points=50, deadline=datetime(2013,11,29))

  #db.session.add(assignment1)
  #db.session.add(assignment2)
  #db.session.add(assignment3)
  #db.session.add(assignment3)
  #db.session.add(assignment4)
  #db.session.add(assignment5)
  #db.session.add(assignment6)
  #db.session.add(assignment7)
  #db.session.add(assignment8)
  #db.session.add(assignment9)
  print colored("Assignments added to database.", "green")

  db.session.commit()

  for assignment in Assignment.query.all():
    if random() > 0.5:
      grade1 = Grade(score=randrange(0,assignment.points))
      test_user1.grades.append(grade1)
      assignment.grades.append(grade1)
      db.session.add(grade1)
    if random() > 0.5:
      grade2 = Grade(score=randrange(0,assignment.points))
      test_user2.grades.append(grade2)
      assignment.grades.append(grade2)
      db.session.add(grade2)
    db.session.add(assignment)

  db.session.add(test_user1)
  db.session.add(test_user2)

  db.session.commit()

  def get_lesson_name_from_file(lesson_file):
    if lesson_file[-5:] == '.html':
      return humanize(lesson_file[:-5])
    else:
      return humanize(lesson_file)

  lesson_root_path = os.path.join('templates', 'gen')
  for lesson_file in sorted(os.listdir(lesson_root_path)):
    lesson_name = get_lesson_name_from_file(lesson_file)
    lesson_link = lesson_file
    lesson = Lesson(name=lesson_name, link=lesson_link)
    lesson_path = os.path.join(lesson_root_path, lesson_file)
    if os.path.isdir(lesson_path):
      for sublesson_file in os.listdir(lesson_path):
        sublesson_name = get_lesson_name_from_file(sublesson_file)
        sublesson_link = os.path.join(lesson_link, clean_filename(sublesson_file))

        # example: mv 0lecture_1.html to lecture1.html
        sublesson_path = os.path.join(lesson_path, sublesson_file)
        clean_sublesson_path = os.path.join(lesson_path, clean_filename(sublesson_file))
        os.system('mv %s %s' % (sublesson_path, clean_sublesson_path))

        sublesson = Sublesson(name=sublesson_name, link=sublesson_link)
        lesson.sublessons.append(sublesson)
    db.session.add(lesson)
  db.session.commit()


  # Add weeks (which contains a lesson and an assignment per week)
  for lesson in Lesson.query.all():
    id = lesson.id
    assignment = Assignment.query.get(id)
    if assignment:
      week = Week(assignment=assignment.id, lesson=lesson.id)
      db.session.add(week)
  db.session.commit()

def add_practice_problems(language):
  lang = Language.query.filter_by(language=language).first()
  if not lang:
    print colored("language %s not found" % language, "red")
  language_id = lang.id

  with settings(warn_only=True):
    os.chdir('practice')
    local('python gen_questions.py %s' % language)
    os.chdir('..')
  practice_problems = json.load(open('practice/%s/practice_problems.json' % language, 'r'))

  # convert all values to strings
  for p in practice_problems:
    for k, v in p.items():
      if not isinstance(v, str) and not isinstance(v, unicode):
        p[k] = json.dumps(v)
  count_add = 0
  count_update = 0
  count_all = 0
  all_problem_names = []
  for problem in practice_problems:
    all_problem_names.append(problem['problem_name'])
    count_all += 1
    start_time = time.time()
    # Get concepts by traversing the ast of the problem's solution
    pt = problem.copy()
    print colored('processing (%s) practice problem %s' % (language, pt['problem_name']), 'blue')
    pt['template_vars'] = utils.get_template_vars(pt['gen_template_vars'])
    pt = utils.get_problem(pt, language_id)
    concept_names = ast_utils.get_concepts(pt['solution'], language_id)
    concepts = []
    for concept_name in concept_names:
      concept = PracticeProblemConcept.query.filter_by(name=concept_name, language_id=language_id).first()
      if concept == None:
        concept = PracticeProblemConcept(name=concept_name, language_id=language_id)
        db.session.add(concept)
        db.session.commit()
      concepts.append(concept)

    problem['is_homework'] = 'homework' in problem
    template = None
    # Create a new template
    if PracticeProblemTemplate.query.filter_by(problem_name=problem['problem_name'], is_current=True, language_id=language_id).count() == 0:
      template = PracticeProblemTemplate(problem_name=problem['problem_name'], prompt=problem['prompt'], solution=problem['solution'], test=problem['test'], hint=problem['hint'], gen_template_vars=problem['gen_template_vars'], concepts=concepts, is_current=True, is_homework=problem['is_homework'], language_id=language_id)
      db.session.add(template)
      print colored("%s added to database." % template.problem_name, 'yellow')
      count_add += 1
    else:
      old_template = PracticeProblemTemplate.query.filter_by(problem_name=problem['problem_name'], is_current=True, language_id=language_id)[0]
      add_new_template = False
      # check if we need to completely scratch the old template and add a new template (the structure of the problem has changed)
      for k in ['prompt', 'solution', 'test']:
        if old_template.to_dict()[k] != problem[k]:
          add_new_template = True
      if add_new_template:
        template = PracticeProblemTemplate(problem_name=problem['problem_name'], prompt=problem['prompt'], solution=problem['solution'], test=problem['test'], hint=problem['hint'], gen_template_vars=problem['gen_template_vars'], concepts=concepts, is_current=True, is_homework=problem['is_homework'], language_id=language_id)
        db.session.add(template)
        print colored("%s added to database." % template.problem_name, 'yellow')
        count_add += 1
        old_template.is_current = False
        if old_template.is_homework:
          homework_problem = HomeworkProblem.query.filter_by(template_id=old_template.id).first()
          db.session.delete(homework_problem)
          db.session.commit()
          print colored("homework problem for old template %s deleted from database." % template.problem_name, 'red')
      else:
        # update template variables, hint if they have been modified
        # we don't need to readd our template in this case
        template = old_template
        count_update_updated = False
        for field_name in ['gen_template_vars', 'hint', 'is_homework']:
          if getattr(template, field_name) != problem[field_name]:
            setattr(template, field_name, problem[field_name])
            print colored("%s updated with changed %s field" % (problem['problem_name'], field_name), 'yellow')
            if not count_update_updated:
              count_update += 1
              count_update_updated = True
    time_spent = time.time() - start_time
    if time_spent > 1:
      print colored('%s took %.2f seconds to generate (more than 1 second is excessive)' % (problem['problem_name'], time_spent), 'red')
    db.session.commit()

    # Add reference to homework if we have a homework problem
    if problem['is_homework']:
      homework = None
      for line in problem['homework'].split('\n'):
        line_split = line.split()
        if line_split[0] == 'week':
          week_num = int(line_split[1])
          homework = Homework.query.filter_by(week=week_num).first()
          if homework == None:
            print colored("homework for week %d does not exist" % week_num, 'red')
            print colored("failed to add homework problem for day %s" % line_split[1], 'red')
            break
        elif line_split[0] == 'day':
          back_day_num = 6 - int(line_split[1])
          back_time = timedelta(back_day_num)
          deadline = homework.deadline - back_time
          homework_problem = HomeworkProblem.query.filter_by(template_id=template.id).first()
          if homework_problem != None:
            if homework_problem.deadline == deadline and homework_problem.homework_id == homework.id:
              print colored("homework problem for template %s already in database for week %d, day %s" % (template.problem_name, homework.week, line_split[1]), 'green')
              continue
            else:
              homework_problem.deadline = deadline
              homework_problem.homework_id = homework.id
              print colored("homework problem for template %s updated to week %d, day %s" % (template.problem_name, homework.week, line_split[1]), 'yellow')
          else:
            homework_problem = HomeworkProblem(deadline=deadline, homework_id=homework.id, template_id=template.id)
          db.session.add(homework_problem);
          print colored("homework problem week %d, day %s added to database" % (homework.week, line_split[1]), 'green')

  count_deleted = 0
  current_problems = PracticeProblemTemplate.query.filter_by(is_current=True, language_id=language_id).all()
  for problem in current_problems:
    if problem.problem_name not in all_problem_names:
      problem.is_current = False
      count_deleted += 1
      print colored("%s deleted from database (set is_current=False)." % problem.problem_name, 'red')

  db.session.commit()

  print colored("%d practice problems processed. %d problems added to database. %d problems updated with changed hint, template or is_homework variable" % (count_all, count_add, count_update), 'green')
  print colored("%d practice problems deleted from database (set is_current=False)" % count_deleted, 'green')

def add_concepts(language):
  lang = Language.query.filter_by(language=language).first()
  if not lang:
    print colored("language %s not found" % language, "red")
  language_id = lang.id

  with settings(warn_only=True):
    os.chdir('practice')
    local('python gen_concepts.py %s' % language)
    os.chdir('..')

  practice_concepts = json.load(open('practice/%s/practice_concepts.json' % language, 'r'))
  concept_count = 0
  all_concepts = PracticeProblemConcept.query.filter_by(language_id=language_id).all()
  for concept in all_concepts:
    concept_obj = practice_concepts[concept.name]
    concept.display_name = concept_obj['display_name']
    concept.explanation = concept_obj['explanation']
    concept_count += 1
  db.session.commit()
  print colored("%d %s concepts updated with display_name and explanation" % (concept_count, language), 'green')


def add_decal_role():
  decal_role = user_datastore.find_role("decal")
  for user in User.query.all():
    print user.id, user.firstname, user.lastname, user.email
    ans = raw_input('Add as DeCal student? [y/n]')
    if ans is 'y':
      user_datastore.add_role_to_user(user, decal_role)
      db.session.add(user)
  db.session.commit()

def email_problems():
  #with Emailer() as emailer:
  subject = 'Your daily problem is here!'
  for user in User.query.filter(User.roles.any(Role.name == 'user'), User.roles.any(Role.name == 'decal')):
    problem_name = get_next_problem(user.id)
    text = "Hi %s!\nHere's todays problem: <a href='/practice/%s/'>%s</a>. Get cracking!\nBen, Lu, and Hurshal" % (user.firstname, problem_name, problem_name)
    #emailer.email_user(user.email, user.firstname, subject, text)

    print colored(problem_name, "yellow"), colored("emailed to user", "green"),
    print colored("%s: %s %s at %s" % (user.id, user.firstname, user.lastname, user.email), "yellow")
    print colored("Subject: %s\nText: %s" % (subject, text), "blue")

def generate_labs():
  if not os.path.exists('static/lab'):
    os.makedirs('static/lab')
  (_,_,labfiles) = os.walk('labs').next()
  for labfile in labfiles:
    lab = open('labs/' + labfile, 'r')
    steps = []
    step = ['']
    pre = False
    code = ''

    i = 0
    lines = lab.readlines()
    if '#%fullscreen' in lines[0]:
      fullscreen_state = 'var lab_fullscreen = true;'
      lines.pop(0)
    else:
      fullscreen_state = 'var lab_fullscreen = false;'
    lines.append('\n')
    for i in range(0, len(lines)):
      line = lines[i]
      if line == '\n':
        if pre:
          step[0] += '</pre>'
          pre = False
        if code:
          step.append(code)
          code = ''
        if step[0]:
          steps.append(step)
          step = ['']
      else:
        if line[0:3] == '###':
          code += line[3:]
        elif line[0] == '#':
          if pre:
            step[0] += '</pre>'
            pre = False
          step[0] += process_line(line[1:].strip()) + '<br/><br/>'
        else:
          if not pre:
            pre = True
            step[0] += '<pre>'
          step[0] += line

    with open('static/lab/' + labfile.replace('.py', '.js'), 'w') as out:
      out.write(fullscreen_state)
      out.write('var lab_content = ')
      out.write(str(steps))
      out.write(';')
  print colored("%s labs generated" % len(labfiles), "green")

def process_line(line):
  if not '`' in line:
    return line

  chunks = line.split('`')
  if len(chunks) % 2 == 0:
    return line

  result = ''
  for i in range(0, len(chunks)):
    result += chunks[i]
    if i % 2 == 0 and i != len(chunks) - 1:
      result += '<code>'
    else:
      result += '</code>'
  return result
