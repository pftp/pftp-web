from cStringIO import StringIO
import sys

# template vars contains a mapping of variables to be replaced in the prompt, solution, and expected from {{ variable_name }} to each value in the list
# e.g. if template vars contains the json {'to_print': ['hello', 'world']}, there will be two problems generated. the first problem will have {{ to_print }} be replaced with hello (no quotes, if you want quotes include it in solution/prompt/expected)
# anything within eval((( anything inside here))) is autoevaluated and returned inside the solution and the result after the template variables are replaced. There will be a regular expression to evalute

def fill_random_template_vars(template, template_vars):
    # not yet implemented
    return template_vars

def replace_template_vars(template, template_vars):
    for template_string, value in template_vars.items():
        template = template.replace('{{ ' + template_string + ' }}', value)
    return template

def eval_template(template):
    while template.find('eval(((') != -1:
        to_eval = template.partition('eval(((')[2].partition(')))')[0]
        evaluated_result = eval(to_eval)
        template = template.replace('eval(((' + to_eval + ')))', str(evaluated_result))
    return template

def get_expected(solution, test):
    old_stdout = sys.stdout
    sys.stdout = StringIo()
    #create expected
    exec(solution + '\n' + test)
    expected = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return expected


def get_problem(prompt, solution, test, hint, template_vars):
    prompt = eval_template(replace_template_vars(problem_info['prompt'], template_vars))
    solution = eval_template(replace_template_vars(problem_info['solution'], template_vars))
    test = replace_template_vars(problem_info['test'], template_vars)
    expected = get_expected(solution, test)
    return prompt, solution, test, expected

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
            expected = get_expected(solution, test)
            hint = problem_info['hint']
            templated_problems.append({'prompt': prompt, 'expected': expected, 'solution': solution, 'test': test, 'hint': hint, 'problem_dir': problem_info['problem_dir']})
    else:
        solution = problem_info['solution']
        test = replace_template_vars(problem_info['test'], template_vars)
        expected = get_expected(solution, test)
        templated_problems.append({'prompt': problem_info['prompt'], 'expected': expected, 'solution': problem_info['solution'], 'test': test, 'hint': hint, 'problem_dir': problem_info['problem_dir']})
    all_problems.append(templated_problems)
print '\n'
for x in all_problems: print x, '\n\n'
practice_problems = open('practice_problems.json', 'w')
practice_problems.write(json.dumps(all_problems))
practice_problems.close()
