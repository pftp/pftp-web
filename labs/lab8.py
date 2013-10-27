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
# Now try running this program from your terminal with a 'grocery_list' file that has a bunch of items in it. Make sure you include poptarts so you can see that thecontained code runs properly!

# You can also read the entire file into a single string using `read`, which can be useful if you want to process the contents of the file as a whole. Here's a really smart program that will tell you when it's time to get groceries. Try it out and be amazed.
groceries = open('grocery_list')
text = groceries.read()
groceries.close()
if len(text) < 10:
  print 'too much work for too little food'
elif len(text) < 100:
  print 'you should probably go get these'
else:
  print 'did you write this while you were hungry?'
# Notice here that we close the file right after we call read because it's contents are in the variable text and we don't need it anymore. Your mom would be happy if you washed your dishes right after eating, and the same thing applies here. When your code is organized and clean, Python is a joy to work with, but if you decide to be sloppy with your coding, then Python will bite you in the ass (pythons are venomous btw).

# Writing to files is similar, but you need to specify that you want to open the file with write permissions, which is done by passing the 'w' option to `open`:
groceries = open('grocery_list', 'w')
foods = ['apples', 'lettuce', 'tomatoes', 'poptarts', 'more poptarts']
for item in foods:
  groceries.write(item)
  groceries.write("\n") #this is the newline character!
groceries.close()
# Note that we are writing a `\n` character after each item. This is how we represent "newlines", which tell the computer or whatever is displaying the string when to start on the next line instead of continuing on the previous one. If we didn't write this to the file in between each food, our file would look like
'appleslettucetomatoespoptarsmore poptarts'
# which is pretty useless as a grocery list.

# Now these features will let you write persistent programs - or programs which remember things in between each time they are run. You've learned about lists which let you store things sequentially, but sometimes you need a different structure to store your information. Let's take a look at dictionaries!
# Dictionaries allow you to store a keyword and an associated value for that keyword. You can access the values in the dictionary through the keyword. 
# First an explanation - these data structures do not contain definitions for every word in the English language. The reason they are called dictionaries is because the method in which data is stored and the method for retrieving data is similar to how you would look up words in a dictionary. When you grab a dictionary looking for the definition of 'kosmokrator', you turn pages until you find 'kosmokrator' and look at the definition that goes with it (n. - the ruler of the world). The Python way of accessing a value would be
print oxford_dictionary['kosmokrator'] #prints "n. - the ruler of the world"
# so in this sense, a dictionary is accessed like a list, except you can give a dictionary any value (string, integer, float, boolean, list!!!) and it'll find the associated value whereas a list only takes integers and finds the value at that location.

# There are 2 ways to create dictionaries, similar to those for lists. You can create a dictionary with values in 1 line like so:
movie_ratings = {'the matrix': 8, 'ice age': 10, 'sharknado': -12}
# or you can create an empty dictionary and add things later like so:
foo = {}
foo['asdf'] = 12
foo[1] = 'baz'
foo['bar'] = {}
foo['bar']['a'] = 'lol nested dictionaries!'
print foo # prints {'asdf': 12, 1: 'baz', 'bar': {'a': 'lol nested dictionaries!'}}

# You can also get a list of all the keys in a dictionary using the `keys` function. This lets you loop over all the data in a dictionary to process or print or what have you:
oxford_dictionary = {'python': 'best language ever', 'benjamin': 'best teacher ever', 'berkekey': 'go beers'}
for word in oxford_dictionary.keys():
  print word, ':', oxford_dictionary[word]

# Now try creating a dictionary with your classes this semester as keys and their times as the values. Then write a loop using `keys` to print out your schedule! Notice that the order that they print is not necessarily the same order as you put them in. This is because dictionaries are used primariy for making these key and value associations, and Python makes no guarantees on the order of the data so entires are likely to be shuffled around.

# Cool now that you have dictionaries in your arsenal of programming prowess, we can take a look at how these structures can be used to communicate information. As you saw last week, processing HTML as strings to pick out data can be a pain in the butt. Luckily, we have JSON. JSON is a standard for storing data as text which is used widely by web applications. You may hear about JSON as a serialization format, which simply means it is a format in which data such as dictionaries or lists can be converted to text and transmitted over the web or stored in a file. We will use this to store some Python dictionaries in a file and then deserialize the text back into a Python dictionary.

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


# Cool! Now that we know how to work with files, store key value pairs, and serialize/deserialize Python values into text that can be put into a file, let's create something that everybody wants - a shitty offline minimally functional version of urban dictionary - or put more practically, a key value pair storage program.
# First, let's think about what this program will need to do and break it into 3 parts:
# 1. The program should read existing JSON data from a text file into a dictionary variable
# 2. The program should let us add and edit values in the dictionary variable
# 3. The program should write whatever changes we made back into the same text file
# Now let's try to write this program by tackling the parts one at a time.

# Let's take a look at the loading portion. We want to account for when Python can't open the text file since it's possible that the file was deleted or never existed. The `isfile` function is useful here. You'll need to import `os.path` to use it like so:
import os.path
if os.path.isfile('data'):
  print 'Yay the file is there!'
else:
  print "poo the file isn't there :("
# Now try writing the loading portion of the program. What we want the loading portion to do is check if the file exists and if so, load its contents into a dictionary, and if not, create an empty dictionary. The example code uses a file named 'data', but you can choose whatever name you like.
# You can test that this portion of the program works by testing it when the text file doesn't exist, and when it contains {"a":1, "b": 2}. Print out the value of the dictionary variable at the end of the loading portion - in the first case it should be empty because the file doesn't exist, and in the second case, it should be exactly that dictionary.

# Once you have that working, let's take a look at the editing portion of the code! What we want the code to do here is add the values we specify to our dictionary variable. Since we don't know how many values we want to add, let's use a `while True` loop and `break` when the user wants to stop adding values. You'll want to use 2 raw_inputs for the key and value, and then set that in the dictionary variable. If the input for the key is "exit", then you should break from the loop. Now try writing the loop for this after the loading portion and verify that it will keep adding values to your dictionary variable until you enter "exit". You can check that everything you typed was added by printing out the dictionary after you break from the loop. Remeber for this part that you shouldn't be touching any files! All you're doing here is editing the Python variable and in the next section 

# Now try adding the saving portion. At this point in the code, you have a dictionary variable with a bunch of data in it, and you want to convert it into JSON and write it back into your data file. Once you get this working, you can take a look at your data file and check if all the things you entered are in it! You should be able to do this multiple times and see that the file changes.

# <b>Checkoff Assignment: </b> Working storage program
# Awesome! You wrote your first program that works with files on your computer! If you want a challenge, try taking this program and extending it so that it will let you view and search the contents of the file.
