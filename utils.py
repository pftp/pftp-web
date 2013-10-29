from cStringIO import StringIO
import sys
from random import randint, choice
# template vars contains a mapping of variables to be replaced in the prompt, solution, and expected from {{ variable_name }} to each value in the list
# e.g. if template vars contains the json {'to_print': ['hello', 'world']}, there will be two problems generated. the first problem will have {{ to_print }} be replaced with hello (no quotes, if you want quotes include it in solution/prompt/expected)
# anything within eval((( anything inside here))) is autoevaluated and returned inside the solution and the result after the template variables are replaced. There will be a regular expression to evalute

RANDOM_INT = range(1, 1000)
RANDOM_SMALL_INT = range(1, 10)
RANDOM_INT_LIST = [[randint(0, 20) for i in range(randint(5, 15)) for x in range(20)]]
RANDOM_STRING_LIST = [x.split() for x in random_sentence]
RANDOM_WORD = ['hello', 'socks', 'benjamin', 'hurshal', 'world', 'moo', 'cow', 'apple', 'banana', 'pumpkin', 'abibliophobia', 'bumbershoot', 'codswallop', 'borborygm', 'batrachomyomachy', 'truffle', 'cherry', 'orange', 'fruit', 'lolipop', 'biscuit', 'manatee', 'ping-pong', 'traffic', 'pop', 'oyster', 'bread', 'pineapple', 'mango', 'kiwi', 'strawberry', 'blueberry', 'raspberry', 'caramel', 'chocolate', 'cookie', 'papaya']
RANDOM_SENTENCE = ['i want it that way', 'breaking bad is awesome', 'terra nova is the best tv show', 'cows moo but chickens bawk', 'bunnies are cute', 'you are my fire my one desire', 'harry potter harry potter ron weasley', 'lol it\'s frodo baggins', "i'm going to make him an offer her can't refuse", 'may the force be with you', "i'll be back", 'mama always said life was like a box of chocolates', 'The best time to plant a tree was 20 years ago The second best time is now', 'mark twain once said something about lightning bugs and lightning']
RANDOM_S_I_DICTIONARY = []

random_type_to_values_list = {'random_int': RANDOM_INT, 'random_small_int': RANDOM_SMALL_INT, 'random_int_list': RANDOM_INT_LIST, 'random_string_list': RANDOM_STRING_LIST, 'random_word': RANDOM_WORD, 'random_sentence': RANDOM_SENTENCE, 'random_s_i_dictionary': RANDOM_S_I_DICTIONARY}

for i in range(20):
    current = {}
    for x in range(randint(3, 6)):
        current[choice(RANDOM_WORD)]= randint(3, 10)
    RANDOM_S_I_DICTIONARY.append(current)

def replace_random_syntax(text, begin):
    random_variable_name = None
    if text.partition(begin)[1] != '':
        random_variable_name = begin.replace('{{ ', '') + text.partition(begin)[2].partition(' }}')[0] # random variable name looks something like random_int:variable_name
        # replace the random variable name for everything
        text = text.replace(random_variable_name, 'REPLACED')
    return text, random_variable_name

def fill_random_template_vars(prompt, solution, test, template_vars):
    text = prompt + '\n' + solution + '\n' + test
    while(true):
        replaced = False
        for random_type, values_list in random_type_to_values_list.items():
            text, random_variable_name = replace_random_syntax(text, '{{ ' + random_type + ':')
            if random_variable_name is not None:
                template_vars[random_variable_name] = choice(values_list)
                replace = True
                continue
        # gone through all of the possible random template tags and found nothing to replace
        if not replaced:
            break
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


def get_problem(prompt, solution, test, template_vars):
    fill_random_template_vars(prompt, solution, test, template_vars)
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
