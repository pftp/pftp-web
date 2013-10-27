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

from application import app, db, user_datastore, Role, User, Assignment, Grade, Lesson, Sublesson, Week, Quiz, QuizQuestion

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
def addquiz1():
  add_quiz1()

@task
def addquiz2():
  add_quiz2()

@task
def addquiz3():
  add_quiz3()

@task
def addassignment5():
  add_assignment5()

@task
def addweek6():
  add_week6()

@task
def addquiz4():
  add_quiz4()

@task
def addweek7():
  add_week7()

@task
def addweek8():
  add_week8()

@task
def adddecalrole():
  add_decal_role()

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
  add_quiz1()
  add_quiz2()
  add_quiz3()
  add_assignment5()
  add_quiz4()

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

  assignment1 = Assignment(name='Homework 1', description='Draw something using at least 3 shapes and 3 colors. Have fun with it!',  points=5, deadline=datetime(2013,9,15,23,59))
  assignment2 = Assignment(name='Homework 2', description='Create a turtle chatbot that can <ul><li>Understand a conversation with at least 3 levels of questions</li><li>Uses a number from raw_input (using the int() conversion)</li><li>Draw something when asked to draw (you can use your Homework 1 submission here!) with something new you learned about turtle graphics from the lab (turtle.write, turtle.circle, etc)</li></ul>', points=5, deadline=datetime(2013,9,22,23,59))
  assignment3 = Assignment(name='Homework 3', description="Draw a scene using at least 3 nested function calls. It should be something that you wouldn't want to try drawing line by line!", points=5, deadline=datetime(2013,9,29,23,59))
  #assignment3 = Assignment(name='Project 1', description='Build a turtle graphics game', points=30, deadline=datetime(2013,10,1))
  #assignment4 = Assignment(name='Homework 3', description='Finish exercises 11-15 before next class',  points=10, deadline=datetime(2013,10,8))
  #assignment5 = Assignment(name='Homework 4', description='Finish exercises 16-20 before next class', points=10, deadline=datetime(2013,10,15))
  #assignment6 = Assignment(name='Project 2', description='Build a Flask app', points=30, deadline=datetime(2013,10,29))
  #assignment7 = Assignment(name='Homework 5', description='Finish exercises 21-25 before next class',  points=10, deadline=datetime(2013,11,5))
  #assignment8 = Assignment(name='Homework 6', description='Finish exercises 26-30 before next class', points=10, deadline=datetime(2013,11,12))
  #assignment9 = Assignment(name='Final Project', description='Build something cool', points=50, deadline=datetime(2013,11,29))

  db.session.add(assignment1)
  db.session.add(assignment2)
  db.session.add(assignment3)
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

def add_quiz1():
  quiz1 = Quiz(name="Week 3 Pop Quiz", week=3)

  question1 = QuizQuestion(question="Which of the following lines would make Winston the Turtle draw a square?", answer_choices=json.dumps([{'id': 'A', 'answer': 't = turtle.Turtle()<br>t.forward(100)<br>t.right(90)<br>t.forward(100)<br>t.right(90)<br>t.forward(100)<br>t.right(90)'}, {'id': 'B', 'answer': 't = turtle.Turtle()<br> t.forward(100)<br> t.right(60)<br>t.forward(100)<br>t.right(60)<br>t.right(100)<br>t.forward(100)'}, {'id': 'C', 'answer': 't = turtle.Turtle()<br>t.forward(100)<br>t.right(60)<br>t.right(30)<br>t.forward(100)<br>t.right(90)<br>t.forward(100)<br>t.right(90)<br>t.forward(100)'}]), solution='C', quiz=quiz1.id)
  question2 = QuizQuestion(question="How do you take 2 numbers as user input and print the two numbers added together?", answer_choices=json.dumps([{'id': 'A', 'answer': 'x=?<br>y=?<br>print x + y'}, {'id': 'B', 'answer': 'x = raw_input("What is first number?")<br> y=raw_input("What is number 2")<br> print x + y'}, {'id': 'C', 'answer': 'x = raw_input("What is the first number?")<br>y=raw_input("What is the second number?")<br>int(x) + int(y)'}, {'id': 'D', 'answer': 'x=raw_input("What is the first number?")<br>y=raw_input("What is the second number?")<br>print int(x) + int(y)'}]), solution='D', quiz=quiz1.id)
  question3 = QuizQuestion(question="What is the proper way to make Winston the Turtle move forward a user inputted number of feet", answer_choices=json.dumps([{'id': 'A', 'answer': 't = turtle.Turtle() <br> t.forward(input)'}, {'id': 'B', 'answer': 't = turtle.Turtle() <br> x = raw_input("How much do you want to go forward") <br> t.forward(x)'}, {'id': 'C', 'answer': 't = turtle.Turtle() <br> x = raw_input("How much do you want to go forward") <br> t.forward(int(t))'}, {'id': 'D', 'answer': 't = turtle.Turtle() <br> y = raw_input("How much do you want to go forward") <br> t.forward(int(y))'}, {'id': 'E', 'answer' : 't = turtle.Turtle() <br> t.forward(raw_input())'}]), solution='D', quiz=quiz1.id)
  question4 = QuizQuestion(question="What will the code below print? <br><br> print 1 + 2", answer_choices=json.dumps([{'id': 'A', 'answer': '5'}, {'id': 'B', 'answer': '3'}, {'id': 'C', 'answer': '7'}, {'id': 'D', 'answer': '12'}]), solution='B', quiz=quiz1.id)
  question5 = QuizQuestion(question="What will the code below print? <br><br> print '1' + '2'", answer_choices=json.dumps([{'id': 'A', 'answer': '5'}, {'id': 'B', 'answer': '3'}, {'id': 'C', 'answer': '7'}, {'id': 'D', 'answer': '12'}]), solution='D', quiz=quiz1.id)

  question10 = QuizQuestion(question="How useful are lectures on a scale from 1-5 (1 being terrible and 5 being good)", answer_choices=json.dumps([{'id': 'A', 'answer': '1'}, {'id': 'B', 'answer': '2'}, {'id': 'C', 'answer': '3'}, {'id': 'D', 'answer': '4'}, {'id': 'E', 'answer' : '5'}]), solution='_', quiz=quiz1.id)
  question11 = QuizQuestion(question="How useful are labs on a scale from 1-5 (1 being terrible and 5 being good)", answer_choices=json.dumps([{'id': 'A', 'answer': '1'}, {'id': 'B', 'answer': '2'}, {'id': 'C', 'answer': '3'}, {'id': 'D', 'answer': '4'}, {'id': 'E', 'answer' : '5'}]), solution='_', quiz=quiz1.id)
  question12 = QuizQuestion(question="What do you think we should spend more time working on and preparing for?", answer_choices=json.dumps([{'id': 'A', 'answer': 'Better Lectures'}, {'id': 'B', 'answer': 'Better Lab'}, {'id': 'C', 'answer': 'Better Homework Assignments'}]), solution='_', quiz=quiz1.id)
  question13 = QuizQuestion(question="How do you feel about the course load?", answer_choices=json.dumps([{'id': 'A', 'answer': 'Too light. I would like to learn more.'}, {'id': 'B', 'answer': 'Just right. I am spending the right amount of time for this class'}, {'id': 'C', 'answer': 'Too much work :('}]), solution='_', quiz=quiz1.id)



  quiz1.questions.append(question1)
  quiz1.questions.append(question2)
  quiz1.questions.append(question3)
  quiz1.questions.append(question4)
  quiz1.questions.append(question5)
  quiz1.questions.append(question10)
  quiz1.questions.append(question11)
  quiz1.questions.append(question12)
  quiz1.questions.append(question13)
  db.session.add(quiz1)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.add(question4)
  db.session.add(question5)
  db.session.add(question10)
  db.session.add(question11)
  db.session.add(question12)
  db.session.add(question13)
  db.session.commit()
  print colored('quiz 1 added to database', "green")

def add_quiz2():
  quiz2 = Quiz(name="Week 4 Pop Quiz", week=4)


  question1 = QuizQuestion(question="What does the following print? <pre>def multiply_by_2(n):\n\treturn n * 2\nprint multiply_by_2(multiply_by_2(multiply_by_2(5)))</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '5'}, {'id': 'B', 'answer': '8'}, {'id': 'C', 'answer': '10'}, {'id': 'D', 'answer': '40'}, {'id': 'E', 'answer': '80'}]), solution='D', quiz=quiz2.id)
  question2 = QuizQuestion(question="What will the following code print? <pre>def fibonacci(n):\n\tif n == 1 or n == 2:\n\t\treturn 1\n\treturn fibonacci(n - 1) + fibonacci(n - 2)\n\nfibonacci(5)</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '1'}, {'id': 'B', 'answer': '2'}, {'id': 'C', 'answer': '3'}, {'id': 'D', 'answer': '4'}, {'id': 'E', 'answer': '5'}, {'id': 'F', 'answer': 'Will not print anything'}]), solution='F', quiz=quiz2.id)
  question3 = QuizQuestion(question="What will the following code print? <pre>def fibonacci(n):\n\tif n == 1 or n == 2:\n\t\treturn 1\n\treturn fibonacci(n - 1) + fibonacci(n - 2)\n\nprint fibonacci(4)</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '1'}, {'id': 'B', 'answer': '2'}, {'id': 'C', 'answer': '3'}, {'id': 'D', 'answer': '4'}, {'id': 'E', 'answer': '5'}, {'id': 'F', 'answer': 'Will not print anything'}]), solution='C', quiz=quiz2.id)
  question4 = QuizQuestion(question="What will the following code print? <pre>def summation(n):\n\tif n < 0:\n\t\treturn 0\n\treturn n + summation(n - 1)\n\nprint summation(7)", answer_choices=json.dumps([{'id': 'A', 'answer': '0'}, {'id': 'B', 'answer': '7'}, {'id': 'C', 'answer': '32'}, {'id': 'D', 'answer': '28'}, {'id': 'E', 'answer': 'Error: this will never return anything.'}]), solution='D', quiz=quiz2.id)
  question5 = QuizQuestion(question="What will the following code print? <pre>def big_summation(n):\n\tif n < 0:\n\t\treturn 0\n\treturn n + summation(n + 1)\n\nprint big_summation(7)", answer_choices=json.dumps([{'id': 'A', 'answer': '0'}, {'id': 'B', 'answer': '7'}, {'id': 'C', 'answer': '32'}, {'id': 'D', 'answer': '28'}, {'id': 'E', 'answer': 'Error: this will never return anything.'}]), solution='E', quiz=quiz2.id)
  question6 = QuizQuestion(question="The code below may have an error. What line is the error on? <pre>def test:\n\treturn 1 + 8 * 9\nprint test()", answer_choices=json.dumps([{'id': 'A', 'answer': 'def test:'}, {'id': 'B', 'answer': 'return 1 + 8 * 9'}, {'id': 'C', 'answer': 'print test()'}, {'id': 'D', 'answer': 'No error!!'}]), solution='A', quiz=quiz2.id)
  question7 = QuizQuestion(question="The code below may have an error. What line is the error on? <pre>def bigger_than_10(n):\n\tif n > 10\n\t\treturn True\n\telse:\n\t\treturn False", answer_choices=json.dumps([{'id': 'A', 'answer': 'def bigger_than_10(n):'}, {'id': 'B', 'answer': 'if n > 10'}, {'id': 'C', 'answer': 'return True'}, {'id': 'D', 'answer': 'else:'}, {'id': 'E', 'answer': 'return False'}, {'id': 'F', 'answer': 'No Error!!'}]), solution='B', quiz=quiz2.id)
  question8 = QuizQuestion(question="What will the following print? <pre> def maybe_make_negative(n, make_negative=False):\n\tif make_negative:\n\t\treturn -1 * n\n\treturn n\nprint maybe_make_negative(5)\nprint maybe_make_negative(6, False)\nprint maybe_make_negative(6, True)\nprint maybe_make_negative(maybe_make_negative(7, True))</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '5<br>6<br>6<br>7'}, {'id': 'B', 'answer': '-5<br>6<br>-6<br>7'}, {'id': 'C', 'answer': '5<br>6<br>-6<br>-7'}, {'id': 'D', 'answer': '5<br>6<br>-6<br>7'}]), solution='C', quiz=quiz2.id)
  question9 = QuizQuestion(question="What will the following print? <pre> print 5 / 2 </pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '2.5'}, {'id': 'B', 'answer': '2'}, {'id': 'C', 'answer': '3'}, {'id': 'D', 'answer': 'This will return an error'}]), solution='B', quiz=quiz2.id)



  quiz2.questions.append(question1)
  quiz2.questions.append(question2)
  quiz2.questions.append(question3)
  quiz2.questions.append(question4)
  quiz2.questions.append(question5)
  quiz2.questions.append(question6)
  quiz2.questions.append(question7)
  quiz2.questions.append(question8)
  quiz2.questions.append(question9)

  db.session.add(quiz2)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.add(question4)
  db.session.add(question5)
  db.session.add(question6)
  db.session.add(question7)
  db.session.add(question8)
  db.session.add(question9)
  db.session.commit()
  print colored('quiz 2 added to database', "green")


def add_quiz3():
  quiz3 = Quiz(name="Week 5 Pop Quiz", week=5)


  question1 = QuizQuestion(question="What does the following print? <pre>def multiply_by_3(n):\n\treturn n * 3\nprint multiply_by_3(multiply_by_3(multiply_by_3(5)))</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '5'}, {'id': 'B', 'answer': '125'}, {'id': 'C', 'answer': '135'}, {'id': 'D', 'answer': '40'}, {'id': 'E', 'answer': '80'}]), solution='C', quiz=quiz3.id)
  question2 = QuizQuestion(question="What will the following code print? <pre>def fibonacci(n):\n\tif n == 1 or n == 2:\n\t\treturn 1\n\treturn fibonacci(n - 1) + fibonacci(n - 2)\n\nprint fibonacci(3)</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '1'}, {'id': 'B', 'answer': '2'}, {'id': 'C', 'answer': '3'}, {'id': 'D', 'answer': '4'}, {'id': 'E', 'answer': '5'}, {'id': 'F', 'answer': 'Will not print anything'}]), solution='B', quiz=quiz3.id)
  question3 = QuizQuestion(question="What will the following code print? <pre>def factorial(n):\n\tif n < 0:\n\t\treturn 1\n\treturn n * factorial(n - 1)\n\nprint factorial(4)", answer_choices=json.dumps([{'id': 'A', 'answer': '0'}, {'id': 'B', 'answer': '12'}, {'id': 'C', 'answer': '24'}, {'id': 'D', 'answer': '48'}, {'id': 'E', 'answer': 'Error: this will never return anything.'}]), solution='C', quiz=quiz3.id)

  question4 = QuizQuestion(question="What will the following print?<br><pre>sum = 0\nfor i in range(1, 10):\n\tsum = sum + i\nprint sum</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '0'}, {'id': 'B', 'answer': '10'}, {'id': 'C', 'answer': '25'}, {'id': 'D', 'answer': '55'}, {'id': 'E', 'answer': 'Error: Will not finish running'}]), solution='D', quiz=quiz3.id)
  question5 = QuizQuestion(question="What will the following print?<br><pre>sum = 0\nwhile(True):\n\tsum = sum  + sum\nprint sum</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '0'}, {'id': 'B', 'answer': '10'}, {'id': 'C', 'answer': '25'}, {'id': 'D', 'answer': '55'}, {'id': 'E', 'answer': 'Error: Will not finish running'}]), solution='E', quiz=quiz3.id)

  quiz3.questions.append(question1)
  quiz3.questions.append(question2)
  quiz3.questions.append(question3)
  quiz3.questions.append(question4)
  quiz3.questions.append(question5)

  db.session.add(quiz3)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.add(question4)
  db.session.add(question5)
  db.session.commit()
  print colored('quiz 3 added to database', "green")




#question1 = QuizQuestion(question="<pre></pre>", answer_choices=json.dumps([{'id': 'A', 'answer': ''}, {'id': 'B', 'answer': ''}, {'id': 'C', 'answer': ''}, {'id': 'D', 'answer': ''}, {'id': 'E', 'answer': ''}]), solution='E', quiz=quiz4.id)
def add_quiz4():
  quiz4 = Quiz(name="Week 7 Pop Quiz", week=7)


  question1 = QuizQuestion(question="What does the following print? <pre>def multiply_by_2(n):\n\treturn n * 2\nprint multiply_by_2(multiply_by_2(multiply_by_2(5)))</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '10'}, {'id': 'B', 'answer': '15'}, {'id': 'C', 'answer': '20'}, {'id': 'D', 'answer': '30'}, {'id': 'E', 'answer': '40'}]), solution='E', quiz=quiz4.id)
  question2 = QuizQuestion(question="What will the following code print? <pre>def fibonacci(n):\n\tif n == 1 or n == 2:\n\t\treturn 1\n\treturn fibonacci(n - 1) + fibonacci(n - 2)\n\nprint fibonacci(2)</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '1'}, {'id': 'B', 'answer': '2'}, {'id': 'C', 'answer': '3'}, {'id': 'D', 'answer': '4'}, {'id': 'E', 'answer': '5'}, {'id': 'F', 'answer': 'Will not print anything'}]), solution='A', quiz=quiz4.id)

  question3 = QuizQuestion(question="What will the following print?<br><pre>sum = 0\nfor i in range(1, 10):\n\tsum = sum + i\nprint sum</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '0'}, {'id': 'B', 'answer': '10'}, {'id': 'C', 'answer': '25'}, {'id': 'D', 'answer': '55'}, {'id': 'E', 'answer': 'Error: Will not finish running'}]), solution='D', quiz=quiz4.id)
  question4 = QuizQuestion(question="What will the following code print?<br><pre>sum = 0\nwhile(True):\n\tsum = sum  + sum\nprint sum</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '0'}, {'id': 'B', 'answer': '10'}, {'id': 'C', 'answer': '25'}, {'id': 'D', 'answer': '55'}, {'id': 'E', 'answer': 'Error: Will not finish running'}]), solution='E', quiz=quiz4.id)
  question5 = QuizQuestion(question="What will the following code print <pre>my_list = [1, 2, 3, 4]\nfor x in my_list:\n\tprint x</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '[1,2,3,4]'}, {'id': 'B', 'answer': '1,<br>2,<br>3,<br>4,'}, {'id': 'C', 'answer': '1<br>2<br>3<br>4'}, {'id': 'D', 'answer': 'This will not print anything'}, {'id': 'E', 'answer': 'None of the above'}]), solution='C', quiz=quiz4.id)
  question6 = QuizQuestion(question="What will the following code print?<pre>my_list = [1,2,3,4]\nfor x in my_list:\n\tprint x * x</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': '[1,2,3,4]'}, {'id': 'B', 'answer': '1,<br>2,<br>3,<br>4,'}, {'id': 'C', 'answer': '1<br>2<br>3<br>4'}, {'id': 'D', 'answer': '1<br>4<br>9<br>16'}, {'id': 'E', 'answer': 'Will not print anything'}]), solution='E', quiz=quiz4.id)
  question7 = QuizQuestion(question="What will the following code print?<pre>a_string = 'Cat in the hat spinning a bat'\nprint a_string.split('in')</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': "['Cat ', 'the hat spinning a bat']"}, {'id': 'B', 'answer': "['Cat ', ' the hat sp', 'n', 'g a bat']"}, {'id': 'C', 'answer': 'Cat<br>the hat spinning a bat'}, {'id': 'D', 'answer': 'Cat<br>the hat sp<br>n<br>g a bat'}]), solution='B', quiz=quiz4.id)
  question8 = QuizQuestion(question="What will the following code print?<pre>a_string = 'Cat in the hat spinning a bat'\nprint a_string.split(' in ')</pre>", answer_choices=json.dumps([{'id': 'A', 'answer': "['Cat ', 'the hat spinning a bat']"}, {'id': 'B', 'answer': "['Cat ', ' the hat sp', 'n', 'g a bat']"}, {'id': 'C', 'answer': 'Cat<br>the hat spinning a bat'}, {'id': 'D', 'answer': 'Cat<br>the hat sp<br>n<br>g a bat'}]), solution='A', quiz=quiz4.id)

  question9 = QuizQuestion(question="Which of the following function returns the title of a webpage which will be enclosed in the &lt;title&gt; &lt;/title&gt; tag? We will call our function like this<pre>\nsome_html = \"&lt;title&gt; This is my title! &lt;/title&gt; This is my webpage.\"\nprint get_title(some_html)</pre>This code should print \"This is my title!\" (Hint string.find('abc') returns the first occurence of 'abc' in your string and returns index (the element number) of 'a'", answer_choices=json.dumps([{'id': 'A', 'answer': 'def get_title(html):<br>&nbsp&nbsp&nbsp return html.get_title()'}, {'id': 'B', 'answer': 'def get_title(html): <br>&nbsp&nbsp&nbsp begin_title = html.find("<title>")<br>&nbsp&nbsp&nbsp end_title = html.find("</title>")<br>&nbsp&nbsp&nbsp return html[begin_title:end_title]'}, {'id': 'C', 'answer': 'def get_title(html): <br>&nbsp&nbsp&nbsp begin_title = html.find("<title>") + 7<br>&nbsp&nbsp&nbsp end_title = html.find("</title>")<br>&nbsp&nbsp&nbsp return html[begin_title:end_title]'}, {'id': 'D', 'answer': 'def get_title(html): <br>&nbsp&nbsp&nbsp begin_title = html.find("<title>")<br>&nbsp&nbsp&nbsp end_title = html.find("</title>") + 8<br>&nbsp&nbsp&nbsp return html[begin_title:end_title]'}]), solution='C', quiz=quiz4.id)


  question10 = QuizQuestion(question="Using our get_title function that we created above, which of the following pieces of code will print the first word in the title tag", answer_choices=json.dumps([{'id': 'A', 'answer': 'print get_title(another_html)[0]'}, {'id': 'B', 'answer': 'print get_title(another_html)[1]'}, {'id': 'C', 'answer': 'title = get_title(another_html)<br>title_split_by_spaces = title.split(' ')<br>print title_split_by_spaces[1]'}, {'id': 'D', 'answer': 'title = get_title(another_html)<br>title_split_by_spaces = title.split(' ')<br>print title_split_by_spaces[0]'}, {'id': 'E', 'answer': 'What?'}]), solution='D', quiz=quiz4.id)


  quiz4.questions.append(question1)
  quiz4.questions.append(question2)
  quiz4.questions.append(question3)
  quiz4.questions.append(question4)
  quiz4.questions.append(question5)
  quiz4.questions.append(question6)
  quiz4.questions.append(question7)
  quiz4.questions.append(question8)
  quiz4.questions.append(question9)
  quiz4.questions.append(question10)


  db.session.add(quiz4)
  db.session.add(question1)
  db.session.add(question2)
  db.session.add(question3)
  db.session.add(question4)
  db.session.add(question5)
  db.session.add(question6)
  db.session.add(question7)
  db.session.add(question8)
  db.session.add(question9)
  db.session.add(question10)
  db.session.commit()
  print colored('quiz 4 added to database', "green")



def add_assignment5():
  assignment5 = Assignment(name='Homework 5', description="""<b> We\'ll be doing our homeworks inside of the terminal from now on!</b> <a href="http://programmingfeelthepower.com/static/assignments/chat_bot.zip"> Click here </a> to download the assignment. chat_bot.zip should be in your Downloads directory now. Unzip the file by double clicking on the chat_bot.zip file and move the folder into your work directory. Type the command <b>cd work/chat_bot</b> to get inside the directory. ls to see what files it contains. Remember, cd means change directory and it's simply a way change folders on your computer. Run the chat_bot program by typing python chat_bot.py into the terminal. If you type "hello" and press RETURN, what happens? What about "bye"? Now try "tell me why".
To quit the program, type "quit". Alternately you can do CTRL+C. In fact, CTRL+C will quit most programs in the Terminal.
<br><br>
Now let\'s see how this stuff works.
The only file you need to edit is "chat_bot.py". Open this file in Aquamacs.
<br><br>
The line "def respond(text):" at the top of the file is a function. Everyting indented after this line is part of the "respond" function. The variable "text" is called an argument to this function. For now, all you need to know is that "text" is a string that the user types as input.
<br><br>
In order to leave a function, we use "return". In addition, our respond function has an output (the response to the input text), so we have to return a response. For example, when we return "hello", our chat bot will respond with "hello" to the given input.
<br><br>
Read through the "respond" function in chat_bot.py line by line. Make sure you understand how literally every line in this function works. If anything is mysterious to you, ask us to explain!
""", points=5, deadline=datetime(2013,9,29,23,59))
  week5 = Week(assignment=assignment5.id, lesson=5)
  db.session.add(assignment5)
  db.session.add(week5)
  db.session.commit()

def add_week6():
  lesson6 = Lesson(name="Week6", link="week6")
  lab6 = Assignment(name="HTML Lab", description="Complete the HTML Lab", points=5, deadline=datetime(2013,10,14,4,59))
  assignment6 = Assignment(name="Homework 6", description="Complete Lab 6 on lists and string manipulation", points=5, deadline=datetime(2013,10,20,23,59))
  db.session.add(lesson6)
  db.session.add(lab6)
  db.session.add(assignment6)
  db.session.commit()
  sublesson6 = Sublesson(name="Lecture 6", link="week6/lecture_6.pdf", lesson_id=lesson6.id)
  week6 = Week(assignment=assignment6.id, lesson=lesson6.id)
  db.session.add(sublesson6)
  db.session.add(week6)
  db.session.commit()

def add_week7():
  lesson7 = Lesson(name="Week7", link="week7")
  lab7 = Assignment(name="Lab 7", description="Complete Lab 7", points=5, deadline=datetime(2013,10,21,4,59))
  db.session.add(lesson7)
  db.session.add(lab7)
  db.session.commit()
  sublesson7 = Sublesson(name="Lecture 7", link="week7/lecture_7.pdf", lesson_id=lesson7.id)
  week7 = Week(assignment=lab7.id, lesson=lesson7.id)
  db.session.add(sublesson7)
  db.session.add(week7)
  db.session.commit()

def add_week8():
  lesson8 = Lesson(name="Week8", link="week8")
  lab8 = Assignment(name="Lab 8", description="Complete Lab 8", points=5, deadline=datetime(2013,10,28,4,59))
  assignment8 = Assignment(name="Homework 8", description="Complete at least 5 out of the 7 dictionary exercises emailed to you each day this week", points=5, deadline=datetime(2013,11,3,23,59))
  db.session.add(lesson8)
  db.session.add(lab8)
  db.session.add(assignment8)
  db.session.commit()
  sublesson8 = Sublesson(name="Lecture 8", link="week8/lecture_8.pdf", lesson_id=lesson8.id)
  week8 = Week(assignment=lab8.id, lesson=lesson8.id)
  db.session.add(sublesson8)
  db.session.add(week8)
  db.session.commit()

def add_decal_role():
  decal_role = user_datastore.create_role(name="decal")
  for user in User.query.all():
    print user.id, user.firstname, user.lastname, user.email
    ans = raw_input('Add as DeCal student? [y/n]')
    if ans is 'y':
      user_datastore.add_role_to_user(user, decal_role)
      db.session.add(user)
  db.session.commit()


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
