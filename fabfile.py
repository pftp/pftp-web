import os
import code
import json
import sqlite3
import markdown
from markdown.postprocessors import Postprocessor
from termcolor import colored
from random import randrange, random
from datetime import datetime

from fabric.api import local, task, settings

from application import app, db, user_datastore, Role, User, Assignment, Grade, Lesson, Sublesson

################################################################################
# Tasks
################################################################################

@task
def clean():
  with settings(warn_only=True):
    local('rm -rf templates/gen')
    local('rm pftp.db')

@task
def build():
  clean()
  generate_pages()
  db.create_all()
  generate_models()
  add_exercises()

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
  code.interact(local=locals())

@task
def run():
  app.run()

@task
def update():
  clean()
  build()

@task(default=True)
def all():
  update()
  run()

################################################################################
# Helpers
################################################################################

def humanize(filename):
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
      output_path = os.path.splitext(os.path.join(output_dir, filename))[0] + '.html'
      input_file = open(input_path, 'r')
      input_text = input_file.read()

      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      output_file = open(output_path, 'w')

      html_output = processor.convert(input_text)

      output_text = markdown_template.replace('[title]', humanize(filename)).replace('[content]', html_output)
      output_file.write(output_text)

      processor.reset()
      count += 1

  print colored("%s files generated" % count, "green")


def generate_models():
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

  assignment1 = Assignment(name='Homework 1', description='Finish exercises 1-5 before next class',  points=10, deadline=datetime(2013,9,10))
  assignment2 = Assignment(name='Homework 2', description='Finish exercises 6-10 before next class', points=10, deadline=datetime(2013,9,17))
  assignment3 = Assignment(name='Project 1', description='Build a turtle graphics game', points=30, deadline=datetime(2013,10,1))
  assignment4 = Assignment(name='Homework 3', description='Finish exercises 11-15 before next class',  points=10, deadline=datetime(2013,10,8))
  assignment5 = Assignment(name='Homework 4', description='Finish exercises 16-20 before next class', points=10, deadline=datetime(2013,10,15))
  assignment6 = Assignment(name='Project 2', description='Build a Flask app', points=30, deadline=datetime(2013,10,29))
  assignment7 = Assignment(name='Homework 5', description='Finish exercises 21-25 before next class',  points=10, deadline=datetime(2013,11,5))
  assignment8 = Assignment(name='Homework 6', description='Finish exercises 26-30 before next class', points=10, deadline=datetime(2013,11,12))
  assignment9 = Assignment(name='Final Project', description='Build something cool', points=50, deadline=datetime(2013,11,29))

  db.session.add(assignment1)
  db.session.add(assignment2)
  db.session.add(assignment3)
  db.session.add(assignment4)
  db.session.add(assignment5)
  db.session.add(assignment6)
  db.session.add(assignment7)
  db.session.add(assignment8)
  db.session.add(assignment9)
  print colored("9 assignments added to database.", "green")

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
    print lesson_name
    lesson_path = os.path.join(lesson_root_path, lesson_file)
    if os.path.isdir(lesson_path):
      for sublesson_file in os.listdir(lesson_path):
        sublesson_name = get_lesson_name_from_file(sublesson_file)
        sublesson_link = os.path.join(lesson_link, sublesson_file)
        sublesson = Sublesson(name=sublesson_name, link=sublesson_link)
        lesson.sublessons.append(sublesson)
    db.session.add(lesson)
  db.session.commit()

def add_exercises():
  exercises_file = open('static/js/practice/exercises.json', 'r')
  exercises = json.loads(exercises_file.read())
  db = sqlite3.connect('pftp.db')
  for ex in exercises:
      db.execute('insert into exercise (prompt, hint, test_cases, ' +
                 'solution) values (?, ?, ?, ?)',
                 [ex['prompt'], ex['hint'], json.dumps(ex['test_cases']),
                     ex['solution']])

  db.commit()
  db.close()
  print colored("%s exercises added to database." % len(exercises), "green")
