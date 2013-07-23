import json
import sqlite3

if __name__ == '__main__':
    exercises_file = open('static/practice/exercises.json', 'r')
    exercises = json.loads(exercises_file.read())
    db = sqlite3.connect('pftp.db')
    for ex in exercises:
        db.execute('insert into exercises (prompt, hint, solution)' +
                   'values (?, ?, ?)',
                   [ex['prompt'], ex['hint'], ex['solution']])
    db.commit()
    db.close()
    print exercises