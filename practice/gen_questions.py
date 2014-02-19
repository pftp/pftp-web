import os
import os.path
import json
import sys
from termcolor import colored

if len(sys.argv) < 2:
  print colored("need language as argument", "red")
  sys.exit(1)

language = sys.argv[1]

PARENT_PROBLEM_DIR = '%s/problems' % language
def read_problem(problem_name):
  problem_path = PARENT_PROBLEM_DIR + '/' + problem_name
  problem_file = open(problem_path, 'r')
  current_key = ''
  current_val = ''
  res = {'problem_name': problem_name.strip(), 'is_homework': 'false'}
  for line in problem_file.readlines():
    if line[:3] == '###':
      if (current_key != ''):
        res[current_key] = current_val.strip()
      current_key = line[3:].strip()
      current_val = ''
    else:
      current_val += line
  if (current_key != ''):
    res[current_key] = current_val.strip()
  problem_file.close()
  return res


""" load the problems """
problem_names = os.listdir(PARENT_PROBLEM_DIR)
all_problems = []
for problem_name in problem_names:
  all_problems.append(read_problem(problem_name))

practice_problems = open('%s/practice_problems.json' % language, 'w')
practice_problems.write(json.dumps(all_problems))
practice_problems.close()
