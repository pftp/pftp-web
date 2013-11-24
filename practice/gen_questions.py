import os
import os.path

import json
import sys
PARENT_PROBLEM_DIR = 'problems'
def read_problem(problem_dir):
  problem_path = PARENT_PROBLEM_DIR + '/' + problem_dir
  problem_file = open(problem_path + '/full_problem', 'r')
  current_key = ''
  current_val = ''
  res = {'problem_dir': problem_dir.strip()}
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
problem_dirs = os.listdir(PARENT_PROBLEM_DIR)
all_problems = []
for problem_dir in problem_dirs:
  all_problems.append(read_problem(problem_dir))

practice_problems = open('practice_problems.json', 'w')
practice_problems.write(json.dumps(all_problems))
practice_problems.close()
