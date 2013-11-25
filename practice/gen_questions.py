import os
import os.path

import json
import sys
PARENT_PROBLEM_DIR = 'problems'
def read_problem(problem_name):
  problem_path = PARENT_PROBLEM_DIR + '/' + problem_name
  problem_file = open(problem_path, 'r')
  current_key = ''
  current_val = ''
  res = {'problem_name': problem_name.strip()}
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

practice_problems = open('practice_problems.json', 'w')
practice_problems.write(json.dumps(all_problems))
practice_problems.close()
