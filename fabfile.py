from fabric.api import local

def build():
  print 'Building site resources'
  local('rm -rf templates/gen')
  local('python build/generate_pages_from_markdown.py')
