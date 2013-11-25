from cStringIO import StringIO
import sys
from random import randint, choice
import json

RANDOM_WORD = ['hello', 'socks', 'benjamin', 'hurshal', 'lu' 'world', 'moo', 'cow', 'apple', 'banana', 'pumpkin', 'abibliophobia', 'bumbershoot', 'codswallop', 'borborygm', 'batrachomyomachy', 'truffle', 'cherry', 'orange', 'fruit', 'lolipop', 'biscuit', 'manatee', 'ping-pong', 'traffic', 'pop', 'oyster', 'bread', 'pineapple', 'mango', 'kiwi', 'strawberry', 'blueberry', 'raspberry', 'caramel', 'chocolate', 'cookie', 'papaya']
RANDOM_SENTENCE = ['i want it that way', 'breaking bad is awesome', 'terra nova is the best tv show', 'cows moo but chickens bawk', 'bunnies are cute', 'you are my fire my one desire', 'harry potter harry potter ron weasley', 'lol its frodo baggins', "im going to make him an offer he cant refuse", 'may the force be with you', "ill be back", 'mama always said life was like a box of chocolates', 'The best time to plant a tree was 20 years ago The second best time is now', 'mark twain once said something about lightning bugs and lightning']
RANDOM_S_I_DICTIONARY = []
for i in range(20):
    current = {}
    for x in range(randint(3, 8)):
        current[choice(RANDOM_WORD)]= randint(3, 10)
    RANDOM_S_I_DICTIONARY.append(current)


# These functions may be used in template generation code in problem files
rand_choice = choice
rand_int = randint

def rand_word():
  return choice(RANDOM_WORD)

def rand_sentence():
  return choice(RANDOM_SENTENCE)

def rand_string_list():
  return choice(RANDOM_SENTENCE).split()

def rand_sidict():
  return choice(RANDOM_S_I_DICTIONARY)

# Replaces all template vars within a template,
# given template string and template_vars dict
def replace_template_vars(template, template_vars):
    for template_string, value in template_vars.items():
        template = template.replace('{{ ' + template_string + ' }}', value if isinstance(value, str) or isinstance(value, unicode) else json.dumps(value))
    return template

# Generates expected output, given solution string and test string
def get_expected(solution, test=''):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    exec(solution + '\n' + test)
    expected = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return expected

# Generates the template vars, given gen_template_vars string from problem file
# Returns a json object
def get_template_vars(gen_template_vars):
  exec_env = globals().copy()
  exec gen_template_vars in exec_env
  return json.dumps(exec_env['res'])

# Generates a problem by filling its templates with template vars and its
# expected fields with expected outputs
def get_problem(problem):
    specific_index = None
    template_vars = json.loads(problem['template_vars'])
    for name in ['prompt', 'solution', 'test', 'hint']:
      problem[name] = replace_template_vars(problem[name], template_vars)
    problem['expected_test'] = get_expected(problem['solution'], problem['test'])
    problem['expected_no_test'] = get_expected(problem['solution'])
    return problem
