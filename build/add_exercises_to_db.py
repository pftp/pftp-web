import json
import sqlite3
from termcolor import colored

"""
Adds all the exercies from the json blob into the database.
Run from fabfile with fab build
"""
if __name__ == '__main__':
    exercises_file = open('static/practice/exercises.json', 'r')
    exercises = json.loads(exercises_file.read())
    db = sqlite3.connect('pftp.db')
    for ex in exercises:
        db.execute('insert into exercises (prompt, hint, test_cases, ' +
                   'solution) values (?, ?, ?, ?)',
                   [ex['prompt'], ex['hint'], json.dumps(ex['test_cases']),
                       ex['solution']])
    db.commit()
    db.close()
    print colored("%s exercises addded to database." % len(exercises), "green")
