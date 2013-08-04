import os
import code
import json
import sqlite3
import markdown
from markdown.postprocessors import Postprocessor
from termcolor import colored

from fabric.api import local, task, settings

import application
from application import app, db, user_datastore, Role, User, Assignment, Grade

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
  context['application'] = application
  code.interact(local=locals())

@task(default=True)
def run():
  app.run()

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
  user_role = Role(name="user")
  admin_role = Role(name="admin")

  admin_user = user_datastore.create_user(email="admin@cramm.it", firstname="Cramm", lastname="It", password="p@ssw0rd")
  admin_user.roles.append(admin_role)

  test_user1 = user_datastore.create_user(email="test@cramm.it", firstname="Test", lastname="User", password="p@ssw0rd")
  test_user1.roles.append(user_role)
  test_user2 = user_datastore.create_user(email="test2@cramm.it", firstname="Test2", lastname="User2", password="p@ssw0rd")
  test_user2.roles.append(user_role)

  db.session.add(admin_user)
  db.session.add(test_user1)
  db.session.add(test_user2)
  print colored("3 users added to database.", "green")

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
  print colored("9 assignments added to database.", "green")

  db.session.commit()

  for assignment in Assignment.query.all():
    grade1 = Grade(score=assignment.points)
    grade2 = Grade(score=assignment.points-5)
    test_user1.grades.append(grade1)
    test_user2.grades.append(grade2)
    assignment.grades.append(grade1)
    assignment.grades.append(grade2)

    db.session.add(grade1)
    db.session.add(grade2)
    db.session.add(assignment)

  db.session.add(test_user1)
  db.session.add(test_user2)

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
