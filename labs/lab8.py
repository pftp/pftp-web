#%fullscreen
# Welcome back! This week's lab will cover file I/O and dictionaries.

# By now you have a good understanding of the basics of Python, and you're ready to start writing some practical programs. If you think about most programs on your computer that you use on a daily basis like a word processor, a browser, and maybe a multimedia player, you'll notice something in common. Yes, it's true that they are all programs, but what we're interested in the program's interaction with files. Most programs have some sort of functionality to open or save files, which corresponds to reading the text from a file, and writing text to a file. When we say file I/O, we mean file INput/OUTput, which is exactly this functionality. Luckily, Python makes this incredibly easy.

# If we take a look at the following code, you'll notice 3 new functions: `open`, `readlines`, and `close`, which do exactly what you would expect them to do. In this example, the `open` takes the location to a file and makes it's contents available under the variable `groceries`. Note that the location here has no slashes in it, so Python will look for a file named 'grocery_list' in the same folder as where the Python code is located. The `readlines` function will take the file and return a list with each line of the file as an element. The `close` command will (surprise surprise) close the file once you're done with it.
groceries = open('grocery_list')
for item in groceries.readlines():
  if 'poptarts' in item:
    print 'I LOVE POPTARTS'      
  else:
    print item
groceries.close()
# Now try running this program from your terminal - remember to create a 'grocery_list' file in the same folder that has a bunch of items in it. Make sure you include poptarts so you can see that the contained code runs properly!

# You can also read the entire file into a single string using `read`, which can be useful if you want to process the contents of the file as a whole. Here's a really smart program that will tell you when it's time to get groceries. Try it out and be amazed.
groceries = open('grocery_list')
text = groceries.read()
groceries.close()
if len(text) < 10:
  print 'too much work for too little food'
elif len(text) < 200:
  print 'you should probably go get these'
else:
  print 'you might need to rent a uhaul for all that stuff'
# Notice here that we close the file right after we call read because it's contents are in the variable text and we don't need it anymore. Your mom would be happy if you washed your dishes right after eating, and the same thing applies here. When your code is organized and clean, programming is easy. If you have unorganized code or you don't understand part of your program then it gets hard.

# Writing to files is similar, but you need to specify that you want to open the file with permissions to write, which is done by passing the 'w' option to `open`:
groceries = open('grocery_list', 'w')
foods = ['apples', 'lettuce', 'tomatoes', 'poptarts', 'more poptarts']
for item in foods:
  groceries.write(item)
  groceries.write("\n") #this is the newline character!
groceries.close()
# Note that we are writing a `\n` character after each item. This is how we represent "newlines", which tell the computer or whatever is displaying the string when to start on the next line instead of continuing on the previous one. If we didn't write this to the file in between each food, our file would look like
'appleslettucetomatoespoptartsmore poptarts'
# which is pretty useless as a grocery list.

# Now these features will let you write persistent programs - or programs which remember things in between each time they are run. You've learned about lists which let you store things sequentially, but sometimes you need a different structure to store your information. Let's take a look at dictionaries!
# Dictionaries allow you to store a keyword and an associated value for that keyword. You can access the values in the dictionary through the keyword. 
# First an explanation - these data structures do not contain definitions for every word in the English language. The reason they are called dictionaries is because the method in which data is stored and the method for retrieving data is similar to how you would look up words in a dictionary. When you grab a dictionary looking for the definition of 'kosmokrator', you turn pages until you find 'kosmokrator' and look at the definition that goes with it (n. - the ruler of the world). The Python way of accessing a dictionary value would be
print oxford_dictionary['kosmokrator'] #prints "n. - the ruler of the world"
# The difference is that Python dictionaries let you use any Python value (string, integer, float, boolean, list, another dictionary!) as the 'key' or 'value' whereas the Oxford Dictionary uses strings for both keys and values.

# There are 2 ways to create dictionaries, similar to those for lists. You can create a dictionary with values in it like so:
movie_ratings = {'the matrix': 8, 'ice age': 10, 'sharknado': -12}
# or you can create an empty dictionary and add things later like so:
foo = {}
foo['asdf'] = 12
foo[1] = 'baz'
foo['bar'] = {}
foo['bar']['a'] = 'lol nested dictionaries!'
print foo # prints {'asdf': 12, 1: 'baz', 'bar': {'a': 'lol nested dictionaries!'}}

# You can also get a list of all the keys in a dictionary using the `keys` function. This lets you loop over all the data in a dictionary to process or print or what have you:
oxford_dictionary = {'python': 'best language ever', 'benjamin': 'best teacher ever', 'berkekey': 'really expensive'}
for word in oxford_dictionary.keys():
  print word, ':', oxford_dictionary[word]
# Python has a shortcut for this which is to omit the `keys` function, but in general it is clearer to include it because then you know the variable you are looping over is a dictionary.
oxford_dictionary = {'python': 'best language ever', 'benjamin': 'best teacher ever', 'berkekey': 'go beers'}
for word in oxford_dictionary:
  print word, ':', oxford_dictionary[word]

# The takeaway from dictionaries is that they are good for storing key-value pairs in no particular order, whereas lists are good at storing single values in a specified order. Now try creating a dictionary with your classes this semester as keys and their times as the values. Then write a loop using `keys` to print out your schedule! Notice that the order that they print is not necessarily the same order as you put them in. This is because dictionaries are used primariy for making these key and value associations, and Python makes no guarantees on the order of the data so entries are likely to be shuffled around.

# Cool now that you have dictionaries in your arsenal of programming prowess, we can take a look at how these structures can be used to communicate information. As you saw last week, processing HTML as strings to pick out data can be a pain in the butt. As always, there is an easier way to deal with this - the JSON format. JSON (JavaScript Object Notation) is a standard for storing data as text which is used widely by web applications. Its name comes from the fact that it is used in Javascript to represent data. Since Javascript is the standard language used by websites to make snazzy animations and features, JSON has become a popular format used to transfer data. You may hear about JSON as a serialization format, which simply means it is a format in which data such as dictionaries or lists can be converted to strings and transmitted over the web or stored in a file as text. We will use this to store some Python dictionaries in a file and then deserialize the text back into Python values.

# Once again Python saves the day as it provides a bunch of convenient JSON functions. The 2 most commonly used are `dumps` and `loads` which take a Python value and convert it into a string in JSON format, and vice versa. Try out the following for different values to get an idea of what JSON looks like. You'll notice that in most simple cases, the JSON text for a value looks exactly like what Python prints out, save for some characters like quotes and newlines which are replaced with their backslash preceding equivalent.
import json
print json.dumps(1)
print json.dumps('asdf')
print json.dumps([1,'foo', 3])
print json.dumps({'a': 1, 'b': 'benjamin', 'c': 'luby tuesday'})
# Also try undoing this operation with `loads` just to convince yourself that it really does convert JSON back into Python values:
print json.loads(json.dumps(1))
print json.loads(json.dumps('asdf'))
print json.loads(json.dumps([1,'foo', 3]))
print json.loads(json.dumps({'a': 1, 'b': 'benjamin', 'c': 'luby tuesday'}))

# Now if you visit <a href="http://programmingfeelthepower.com/api.public/course_info">http://programmingfeelthepower.com/api.public/course_info</a>, you can see JSON in the wild! We have added this 'endpoint' or URL to our website which takes all the information available on the class schedule and formats it as JSON. If you paste the URL into JSON data URL on <a href='http://jsonformatter.curiousconcept.com/'>JSON Formatter</a> and click Process, you can see a formatted version of the JSON and explore the structure of it. One you do that, here's how you could take this url, download the JSON text, and convert the text back into Python values:
import urllib2
import json
page = urllib2.urlopen('http://programmingfeelthepower.com/api.public/course_info') #download the page
json_text = page.read() #get the page contents as string
data = json.loads(json_text) #deserialize the JSON
print 'Title: ', data['title'] #string
print 'Course: ', data['course'] #string
print 'Units: ', data['units'] #string
print 'Schedule: ', data['schedule'] #list!
# At this point you could write a program to remind you when homework is due because you have all the deadlines in the data.

# Cool! Now that we know how to work with files, store key value pairs, and serialize/deserialize Python values into text that can be put into a file, let's create something that everybody wants - a minimally functional notepad program. It will let you save Python dictionaries as text and then edit them later.
# First, let's think about what this program will need to do and break it into 3 parts:
# 1. The program should read existing JSON data from a text file into a dictionary variable
# 2. The program should let us add and edit values in the dictionary variable
# 3. The program should write whatever changes we made back into the same text file
# As you write more and more complex programs, you'll start to run into a problem - after a certain size, it becomes impossible to mentally track an entire program. This is where abstraction is crucial. We have broken the program into 3 separate parts, and by thinking about each part separately, we can minimize the amount of code that we need to keep track of at any given time. We have made a couple assumptions that make this possible. When we are writing the second part of the program, we assume that the first part did its job and has created a dictionary variable that we can edit. When we are writing the third part of the program, we assume that the second part saved all the changes that the user wanted to make and now all we have to worry about is saving the contents to a file.
# Now let's try to write this program by tackling the parts one at a time.

# Let's take a look at the loading portion. We want to account for when Python can't open the text file since it's possible that the file was deleted or never existed. The `isfile` function is useful here. You'll need to import `os.path` to use it like so:
import os.path
if os.path.isfile('data'):
  print 'Yay the file is there!'
else:
  print "poo the file isn't there :("
# Now try writing the loading portion of the program. What we want the loading portion to do is check if the file exists and if so, load its contents into a dictionary, and if not, create an empty dictionary to work with. In either case, the dictionary variable will be edited and saved - creating the missing file if necessary. The example code uses a file named 'data', but you can choose whatever name you like.
# You can test that this portion of the program works by testing it when the text file doesn't exist, and when it contains {"a":1, "b": 2}. Print out the value of the dictionary variable at the end of the loading portion - in the first case it should be empty because the file doesn't exist, and in the second case, it should look something like {u'a':1, u'b':2} (the u before the quotes means its a special type of string, but for our purposes this doesn't affect the program).

# Once you have that working, let's take a look at the editing portion of the code! What we want the code to do here is add the values we specify to our dictionary variable. Since we don't know how many values we want to add, let's use a `while True` loop and `break` when the user wants to stop adding values. You'll want to use 2 raw_inputs for the key and value, and then set that in the dictionary variable. If the input for the key is "exit", then you should break from the loop. Now try writing the loop for this after the loading portion and verify that it will keep adding values to your dictionary variable until you enter "exit". You can check that everything you typed was added by printing out the dictionary after you break from the loop. Remember for this part that you shouldn't be touching any files! All you're doing here is editing the Python variable.

# Now try adding the saving portion. At this point in the code, you have a dictionary variable with a bunch of data in it, and you want to convert it into JSON and write it back into your data file. Once you get this working, you can take a look at your data file and check if all the things you entered are in it! You should be able to do this multiple times and see that the file changes.

# <b>Checkoff Assignment: </b> Working notepad program
# Awesome! You wrote your first program that works with files on your computer! If you want a challenge, try taking this program and extending it so that it will let you view and search the contents of the file. You can use something like
if 'key1' in data:
  print data['key1']
else:
  print 'key1 is not in the dictionary!'
# to check if a key is currently in the dictionary or not.
