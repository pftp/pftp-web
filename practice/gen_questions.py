import os
import os.path

import json
import sys
PARENT_PROBLEM_DIR = 'problems'
def read_problem(problem_dir):
    problem_path = PARENT_PROBLEM_DIR + '/' + problem_dir
    prompt = open(problem_path + '/prompt', 'r').read()
    #expected = open(problem_path + '/expected', 'r').read()
    solution = open(problem_path + '/solution.py', 'r').read()
    test= open(problem_path + '/test.py', 'r').read()
    hint = open(problem_path + '/hint', 'r').read()
    if os.path.isfile(problem_path + '/template_vars.json'):
        template_vars = json.load(open(problem_path + '/template_vars.json', 'r'))
    else:
        template_vars = {}
    return {'prompt': prompt.strip(), 'solution': solution.strip(), 'test': test.strip(), 'hint': hint.strip(), 'template_vars': template_vars, 'problem_dir': problem_dir.strip()}



""" load the problems """
problem_dirs = os.listdir(PARENT_PROBLEM_DIR)
all_problems = []
for problem_dir in problem_dirs:
    all_problems.append(read_problem(problem_dir))

practice_problems = open('practice_problems.json', 'w')
practice_problems.write(json.dumps(all_problems))
practice_problems.close()
