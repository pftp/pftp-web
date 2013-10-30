from cStringIO import StringIO
import sys
from random import randint, choice
import json
# template vars contains a mapping of variables to be replaced in the prompt, solution, and expected from {{ variable_name }} to each value in the list
# e.g. if template vars contains the json {'to_print': ['hello', 'world']}, there will be two problems generated. the first problem will have {{ to_print }} be replaced with hello (no quotes, if you want quotes include it in solution/prompt/expected)
# anything within eval((( anything inside here))) is autoevaluated and returned inside the solution and the result after the template variables are replaced. There will be a regular expression to evalute

RANDOM_INT = range(1, 1000)
RANDOM_SMALL_INT = range(1, 10)
RANDOM_INT_LIST = [[randint(0, 20) for i in range(randint(5, 15)) for x in range(20)]]

RANDOM_WORD = ['hello', 'socks', 'benjamin', 'hurshal', 'world', 'moo', 'cow', 'apple', 'banana', 'pumpkin', 'abibliophobia', 'bumbershoot', 'codswallop', 'borborygm', 'batrachomyomachy', 'truffle', 'cherry', 'orange', 'fruit', 'lolipop', 'biscuit', 'manatee', 'ping-pong', 'traffic', 'pop', 'oyster', 'bread', 'pineapple', 'mango', 'kiwi', 'strawberry', 'blueberry', 'raspberry', 'caramel', 'chocolate', 'cookie', 'papaya']
RANDOM_SENTENCE = ['i want it that way', 'breaking bad is awesome', 'terra nova is the best tv show', 'cows moo but chickens bawk', 'bunnies are cute', 'you are my fire my one desire', 'harry potter harry potter ron weasley', 'lol it\'s frodo baggins', "i'm going to make him an offer her can't refuse", 'may the force be with you', "i'll be back", 'mama always said life was like a box of chocolates', 'The best time to plant a tree was 20 years ago The second best time is now', 'mark twain once said something about lightning bugs and lightning']
RANDOM_STRING_LIST = [x.split() for x in RANDOM_SENTENCE]
RANDOM_S_I_DICTIONARY = []

random_type_to_values_list = {'random_int': RANDOM_INT, 'random_small_int': RANDOM_SMALL_INT, 'random_int_list': RANDOM_INT_LIST, 'random_string_list': RANDOM_STRING_LIST, 'random_word': RANDOM_WORD, 'random_sentence': RANDOM_SENTENCE, 'random_s_i_dictionary': RANDOM_S_I_DICTIONARY}

for i in range(20):
    current = {}
    for x in range(randint(3, 8)):
        current[choice(RANDOM_WORD)]= randint(3, 10)
    RANDOM_S_I_DICTIONARY.append(current)


def replace_random_syntax(text, begin):
    random_variable_name = None
    if text.partition(begin)[1] != '':
        random_variable_name = begin.replace('{{ ', '') + text.partition(begin)[2].partition(' }}')[0] # random variable name looks something like random_int:variable_name
        # replace the random variable name for everything
        text = text.replace(random_variable_name, 'REPLACED')
    return text, random_variable_name

def get_random_template_vars(prompt, solution, test, template_vars):
    chosen_vars = []
    text = prompt + '\n' + solution + '\n' + test
    while(True):
        replaced = False
        for random_type, values_list in random_type_to_values_list.items():
            text, random_variable_name = replace_random_syntax(text, '{{ ' + random_type + ':')
            if random_variable_name is not None:
                while True:
                    # we want unique variables
                    chosen_var = choice(values_list)
                    if chosen_var not in chosen_vars:
                        chosen_vars.append(chosen_var)
                        template_vars[random_variable_name] = [chosen_var,]
                        break
                replaced = True
                break
        # gone through all of the possible random template tags and found nothing to replace
        if not replaced:
            break
    return template_vars

def choose_nonrandom_template_vars(template_vars, specific_index):
    for template_string, value in template_vars.items():
        if len(value) != 1:
            template_vars[template_string] = [value[specific_index]]
    return template_vars


def replace_template_vars(template, template_vars):
    for template_string, value in template_vars.items():
        value = value[0]
        template = template.replace('{{ ' + template_string + ' }}', value if isinstance(value, str) or isinstance(value, unicode) else json.dumps(value))
    return template

def eval_template(template):
    while template.find('eval(((') != -1:
        to_eval = template.partition('eval(((')[2].partition(')))')[0]
        evaluated_result = eval(to_eval)
        template = template.replace('eval(((' + to_eval + ')))', str(evaluated_result))
    return template

def get_expected(solution, test=''):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    #create expected
    exec(solution + '\n' + test)
    expected = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return expected


def get_problem(problem, fill_random=True):
    specific_index = None
    if fill_random:
        problem['template_vars'] = json.loads(problem['template_vars'])
        if len(problem['template_vars']) > 0:
            specific_index = randint(0, len(problem['template_vars'].values()[0]) - 1)
        problem['template_vars'] = get_random_template_vars(problem['prompt'], problem['solution'], problem['test'], problem['template_vars'])
        problem['template_vars'] = choose_nonrandom_template_vars(problem['template_vars'], specific_index)
    else:
        problem['template_vars'] = json.loads(problem['template_vars'])
    problem['prompt'] = eval_template(replace_template_vars(problem['prompt'], problem['template_vars']))
    problem['solution'] = eval_template(replace_template_vars(problem['solution'], problem['template_vars']))
    problem['test'] = replace_template_vars(problem['test'], problem['template_vars'])
    problem['hint'] = replace_template_vars(problem['hint'], problem['template_vars'])
    problem['expected_test'] = get_expected(problem['solution'], problem['test'])
    problem['expected_no_test'] = get_expected(problem['solution'])
    return problem
