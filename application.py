import os
import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, g, Markup

DATABASE = 'pftp.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
  return 'This is Programming Feel The Power'

@app.route('/practice/ex<int:ex_id>')
def practice(ex_id):
    ex_row = g.db.execute(
        'select * from exercises where id = ?', [str(ex_id)]
    ).fetchone()
    if ex_row is not None:
        ex = dict(ex_row)
        ex['hint'] = Markup(ex['hint'])
        return render_template('practice.html', ex=ex)
    else:
        return redirect('/practice/ex1')

@app.route('/lessons/<path>')
def lesson(path):
  filepath = os.path.join('gen', path)
  if os.path.exists(os.path.join('templates', filepath)):
    return render_template(filepath)
  else:
    return redirect('/')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
  app.run(debug=True)
