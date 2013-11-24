# USAGE: python make_full_problem.py <problem_dir>

import os
import os.path
import sys

problem_path = sys.argv[1]
if problem_path[-1] == '/':
  problem_path = problem_path[:-1]
res_file = open(problem_path + '/full_problem', 'w')
for name in ['prompt', 'solution', 'test', 'hint', 'template_vars']:
  fname = name
  if name in ['solution', 'test']:
    fname += '.py'
  elif name == 'template_vars':
    fname += '.json'
  cur_file = open(problem_path + '/' + fname, 'r')
  res_file.write('### ' + name + '\n')
  res_file.write(cur_file.read() + '\n')
  cur_file.close()
res_file.close()

