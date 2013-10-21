import urllib2

department = raw_input('What department do you want to search in? Make sure you put the department name as listed in schedule.berkeley.edu!\n')
deptname = department.replace(' ', '+')
url = 'http://osoc.berkeley.edu/OSOC/osoc?p_term=SP&p_deptname=' + deptname + '&p_start_row='
print 'Scraping schedule.berkeley.edu for courses in ' + department + ' department...'

row = 1
start = '<B>' + department.upper()
end = '</B>'
print start, end
while True:
  html = urllib2.urlopen(url + str(row)).read().upper()
  if html.find(start) != -1:
    break

  while True:
    i = html.find(start)
    j = html[i:].find(end)
    if i == -1 or j == -1:
      #no more matches
      break
    else:
      print html[i+3:i+j]
      html = html[i+j:]
  row = row + 100
