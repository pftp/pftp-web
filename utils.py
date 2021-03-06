from cStringIO import StringIO
import sys
from random import random, randint, choice
import json
import subprocess
import tempfile
import os

RANDOM_WORD = ['hello', 'socks', 'benjamin', 'hurshal', 'lu' 'world', 'moo', 'cow', 'apple', 'banana', 'pumpkin', 'abibliophobia', 'bumbershoot', 'codswallop', 'borborygm', 'batrachomyomachy', 'truffle', 'cherry', 'orange', 'fruit', 'lolipop', 'biscuit', 'manatee', 'pingpong', 'traffic', 'pop', 'oyster', 'bread', 'pineapple', 'mango', 'kiwi', 'strawberry', 'blueberry', 'raspberry', 'caramel', 'chocolate', 'cookie', 'papaya']
RANDOM_SENTENCE = ['i want it that way', 'breaking bad is awesome', 'terra nova is the best tv show', 'cows moo but chickens bawk', 'bunnies are cute', 'you are my fire my one desire', 'harry potter harry potter ron weasley', 'lol its frodo baggins', "im going to make him an offer he cant refuse", 'may the force be with you', "ill be back", 'mama always said life was like a box of chocolates', 'The best time to plant a tree was 20 years ago The second best time is now', 'mark twain once said something about lightning bugs and lightning']

# These functions may be used in template generation code in problem files
rand_choice = choice
rand_int = randint

def rand_letter():
  ascii_val = 0
  if random() < 0.5:
    ascii_val = randint(65, 90)
  else:
    ascii_val = randint(97, 122)
  return chr(ascii_val)

def rand_char():
  return chr(randint(32, 126))

def rand_word():
  return choice(RANDOM_WORD)

def rand_sentence():
  return choice(RANDOM_SENTENCE)

def rand_string():
  res = rand_sentence()
  for i in range(rand_int(0, 5)):
    idx = rand_int(0, len(res)-1)
    res = res[:idx] + rand_char() + res[idx:]
  return res

def rand_word_list(n):
  res = []
  for i in range(n):
    res.append(rand_word())
  return res

def rand_word_list_list(n):
  res = []
  for i in range(n):
    res.append(rand_word_list(randint(1, 10)))
  return res

def rand_sentence_list(n):
  res = []
  for i in range(n):
    res.append(rand_sentence())
  return res

def rand_string_list(n):
  res = []
  for i in range(n):
    res.append(rand_string())
  return res

def rand_int_list(n):
  res = []
  for i in range(n):
    res.append(randint(-100, 100))
  return res

def rand_int_list_list(n):
  res = []
  for i in range(n):
    res.append(rand_int_list(randint(1, 10)))
  return res


def rand_sidict():
  res = {}
  for i in range(20):
    res[choice(RANDOM_WORD)] = randint(-100, 100)
  return res

def nth(n):
  nth = str(n)
  if nth[-1] == '1' and (len(nth) < 2 or nth[-2] != '1'):
    nth += 'st'
  elif nth[-1] == '2' and (len(nth) < 2 or nth[-2] != '1'):
    nth += 'nd'
  elif nth[-1] == '3' and (len(nth) < 2 or nth[-2] != '1'):
    nth += 'rd'
  else:
    nth += 'th'
  return nth

# Replaces all template vars within a template,
# given template string and template_vars dict
def replace_template_vars(template, template_vars):
  for template_string, value in template_vars.items():
      template = template.replace('{{ ' + template_string + ' }}', value if isinstance(value, str) or isinstance(value, unicode) else json.dumps(value))
  return template

# Generates expected output, given solution string and test string
def get_expected(solution, language_id, test=''):
  #TODO detect language automatically
  if language_id == 1:
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    exec(solution + '\n' + test, {})
    expected = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return expected
  elif language_id == 2:
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(solution + '\n' + test)
    tmp.close()
    process = subprocess.Popen(['node', tmp.name], stdout=subprocess.PIPE)
    out, err = process.communicate()
    os.unlink(tmp.name)
    return out

# Generates the template vars, given gen_template_vars string from problem file
# Returns a json object
def get_template_vars(gen_template_vars):
  exec_env = globals().copy()
  exec gen_template_vars in exec_env
  return json.dumps(exec_env['res'])

# Generates a problem by filling its templates with template vars and its
# expected fields with expected outputs

def get_problem(problem, language_id):
  specific_index = None
  template_vars = json.loads(problem['template_vars'])
  for name in ['prompt', 'solution', 'test', 'hint']:
    problem[name] = replace_template_vars(problem[name], template_vars)
  problem['expected_test'] = get_expected(problem['solution'], language_id, problem['test'])
  problem['expected_no_test'] = get_expected(problem['solution'], language_id)
  return problem
