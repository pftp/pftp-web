from fabric.api import local

def build():
  print 'Building site resources'
  local('rm -rf templates/gen')
  local('python build/generate_pages_from_markdown.py')
  local('rm pftp.db')
  local('sqlite3 pftp.db < schema.sql')
  local('python build/add_exercises_to_db.py')
