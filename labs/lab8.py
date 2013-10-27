import os.path
import json

data = {}

#check if files exists
if os.path.isfile('data'):
  with open('data') as file:
    print 'Old file contents:'
    contents = file.read()
    print contents
    ans = raw_input('Do you want to:\n 1) edit this data\n 2) start over? [1/2]')
    if ans is '1':
      data = json.loads(contents)
else:
  print 'No file detected. New one will be created'

with open('data', 'w') as file:
  print 'Start entering data to be saved in file!'
  while True:
    key = raw_input('Enter keyword or exit: ')
    if key in 'exit':
      break
    else:
      val = raw_input('Enter value for keyword %s: ' % key)
      #store data
      data[key] = val
  
  file.write(json.dumps(data)) 
  print 'Data saved!'
