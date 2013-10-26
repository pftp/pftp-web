import os

def read_question(question_path):
    expected = open(question_path + '/expected', 'r').read()
    prompt = open(question_path + '/prompt', 'r').read()
    solution = open(question_path + '/solution.py', 'r').read()
    hint = open(question_path + '/hint', 'r').read()
    return {'expected': expected, 'prompt': prompt, 'solution': solution, 'hint': hint}


question_dirs = os.listdir('questions')
all_questions = []
for question_dir in question_dirs:
    all_questions.append(read_question('questions/' + question_dir))

print all_questions
