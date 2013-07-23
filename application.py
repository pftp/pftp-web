import os
from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return 'This is Programming Feel The Power'

@app.route('/practice')
def practice():
    return render_template('practice.html')

@app.route('/lessons/<path>')
def lesson(path):
  filepath = os.path.join('gen', path)
  if os.path.exists(os.path.join('templates', filepath)):
    return render_template(filepath)
  else:
    return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
