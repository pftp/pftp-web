import os
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
    template_vars = json.load(open(problem_path + '/template_vars.json', 'r'))
    return {'prompt': prompt, 'solution': solution, 'test': test, 'hint': hint, 'template_vars': template_vars, 'problem_dir': problem_dir}



""" load the problems """
problem_dirs = os.listdir(PARENT_PROBLEM_DIR)
all_problem_info = []
for problem_dir in problem_dirs:
    all_problem_info.append(read_problem(problem_dir))


# created all problems with their templates
# template vars contains a mapping of variables to be replaced in the prompt, solution, and expected from {{ variable_name }} to each value in the list
# e.g. if template vars contains the json {'to_print': ['hello', 'world']}, there will be two problems generated. the first problem will have {{ to_print }} be replaced with hello (no quotes, if you want quotes include it in solution/prompt/expected)
# anything within eval((( anything inside here))) is autoevaluated and returned inside the solution and the result after the template variables are replaced. There will be a regular expression to evalute

def eval_template(template):
    while template.find('eval(((') != -1:
        to_eval = template.partition('eval(((')[2].partition(')))')[0]
        evaluated_result = eval(to_eval)
        template = template.replace('eval(((' + to_eval + ')))', str(evaluated_result))
    return template


def replace_template_vars(template, template_vars):
    for template_string, value in template_vars.items():
        template = template.replace('{{ ' + template_string + ' }}', value)
    return template


""" generate the problems using templating """
all_problems = []

for problem_info in all_problem_info:
    templated_problems = []
    # {'variable':['val1', 'val2'], 'variable2': ['val3', val4']} to {'variable1': 'val1', 'variable2': 'val3'} and {'variable1': 'val2', 'variable2': 'val4'}
    if len(problem_info['template_vars'].values()) != 0:
        template_vars = {}
        for i in range(len(problem_info['template_vars'].values()[0])):
            for variable, values in problem_info['template_vars'].items():
                template_vars[variable] = values[i]
            prompt = eval_template(replace_template_vars(problem_info['prompt'], template_vars))
            #expected = eval_template(replace_template_vars(problem_info['expected'], template_vars))
            solution = eval_template(replace_template_vars(problem_info['solution'], template_vars))
            test = replace_template_vars(problem_info['test'], template_vars)
            temp = sys.stdout
            sys.stdout = open(PARENT_PROBLEM_DIR + '/' + problem_info['problem_dir'] + '/expected', 'w')
            #create expected
            exec(solution + '\n' + test)
            sys.stdout = temp
            expected = open(PARENT_PROBLEM_DIR +'/' + problem_info['problem_dir'] + '/expected', 'r').read()
            hint = problem_info['hint']
            templated_problems.append({'prompt': prompt, 'expected': expected, 'solution': solution, 'test': test, 'hint': hint, 'problem_dir': problem_info['problem_dir']})
    else:
        solution = problem_info['solution']
        test = replace_template_vars(problem_info['test'], template_vars)
        temp = sys.stdout
        sys.stdout = open(PARENT_PROBLEM_DIR + '/' + problem_info['problem_dir'] + '/expected', 'w')
        #create expected
        exec(problem_info['solution'] + '\n' + test)
        sys.stdout = temp


        templated_problems.append({'prompt': problem_info['prompt'], 'solution': problem_info['solution'], 'test': test, 'problem_dir': problem_info['problem_dir']})
    all_problems.append(templated_problems)
print '\n'
for x in all_problems: print x, '\n\n'
