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

from application import app, db, user_datastore, Role, User, Assignment, Grade, Lesson, Sublesson, Week

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
def genlabs():
  generate_labs()

@task
def build():
  clean()
  generate_pages()
  generate_labs()
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

@task(default=True)
def run():
  app.run()

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

  assignment1 = Assignment(name='Homework 1', description='Draw something using at least 3 shapes and 3 colors. Have fun with it!',  points=10, deadline=datetime(2013,9,15,23,59))
  lab1 = Assignment(name='Lab 1', description='Complete Lab 1',  points=10, deadline=datetime(2013,9,16,12,59))
  #assignment2 = Assignment(name='Homework 2', description='Finish exercises 6-10 before next class', points=10, deadline=datetime(2013,9,17))
  #assignment3 = Assignment(name='Project 1', description='Build a turtle graphics game', points=30, deadline=datetime(2013,10,1))
  #assignment4 = Assignment(name='Homework 3', description='Finish exercises 11-15 before next class',  points=10, deadline=datetime(2013,10,8))
  #assignment5 = Assignment(name='Homework 4', description='Finish exercises 16-20 before next class', points=10, deadline=datetime(2013,10,15))
  #assignment6 = Assignment(name='Project 2', description='Build a Flask app', points=30, deadline=datetime(2013,10,29))
  #assignment7 = Assignment(name='Homework 5', description='Finish exercises 21-25 before next class',  points=10, deadline=datetime(2013,11,5))
  #assignment8 = Assignment(name='Homework 6', description='Finish exercises 26-30 before next class', points=10, deadline=datetime(2013,11,12))
  #assignment9 = Assignment(name='Final Project', description='Build something cool', points=50, deadline=datetime(2013,11,29))

  db.session.add(assignment1)
  db.session.add(lab1)
  #db.session.add(assignment2)
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
    week = Week(assignment=assignment.id, lesson=lesson.id)
    db.session.add(week)
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
