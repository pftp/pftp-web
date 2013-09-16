# Welcome back! This time, you'll be chatting with Winston and helping him draw shapes!
# If you remember from last lab, Winston can draw a square if you tell him the right things, but this isn't the easiest code to edit. Right now, What if you want to make the square smaller? You might have run into this kind of problem while doing the homework - It's kind of annoying to edit all 4 `winston.forward(100)` lines to `winston.forward(60)` and it can get pretty tedious when you have a bunch of shapes that you want to change.
###import turtle
###winston = turtle.Turtle()
###winston.forward(100)
###winston.right(90)
###winston.forward(100)
###winston.right(90)
###winston.forward(100)
###winston.right(90)
###winston.forward(100)
###winston.right(90)

# We're big believers in "learning through pain", so we intentionally left out the key construct in programming that would allow you to circumvent this problem.
# Do you want to know how to do it? Yes?
# Ok good because programming is chock full of these powerful and time-saving ideas and constructs, so you should prepare yourself for the ride.

# Introducing variables, an integral part of programming that can and will save you lots of time editing values in your code.
# The way variables work is simple: Each variable has a name, and a value which you can set and get.
# Note that variable names can only contain letters, numbers, and underscores but cannot start with a number.
foo = 60
# Then you can 'get' it's value by just typing it's name. Python will interpret that and replace it with it's value before running the code.
# So wherever you would use a number in your code, you can use `foo` as well!
foo + 12 # this is 72
###

# You can use the `print` command to display the value of things. In Python, a print statement looks like `print <value>` where <value> is either a literal value, the name of a variable, or an expression including the two that evaluates to a value:
print 12.5
print bar
print foo + 16
# Now you try creating a variable named `bar` and set it's value to be 42. Then create another variable named `baz` and set it's value to be twice the value of `bar` plus 17.

# Great! Let's revisit our square code! Since we are trying to draw a square, we want all 4 `winston.forward`s to move the same distance. We can use the same variable to represent that distance!
size = 100
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
# All that changed was that there is now a variable defined at the top and we use this variable for all the `winston.forward`s.
# This will draw the same square that we originally had, but what if we want to change the size of the square now?

# All we have to do is change the value of size, and all the `winston.forward`s will use the new number!
size = 42
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
# so by using the same variable for all 4 lines, we reduced the number of lines needing editing from 4 to 1.
# Now that may not seem like much, but consider a regular enneacontagon (a 90-sided polygon) where changing it's size without variables would require changing 90 `winston.forward` lines versus changing just 1 variable if you programmed it like the square above.

# Now you try it out with a hexagon! You should be able to change the size of the hexagon by editing a single line (hint: you'll need a variable!)

# Awesome! Now with variables under our belts, let's learn how to communicate with Winston.
# Winston lives inside the world of Python, but he only talk to us through the `print` statement.
print 'Hi, my name is Winston!'
# Or you can print multiple values in a row by separating them with commas:
print 'Hi,', 'my', 'name', 'is', 'Winston!'

# You can talk to Winston using the `raw_input` statement. Since Winston lives in Python, your message to Winston needs to be saved into a variable:
message = raw_input('Say hi to Winston!')
print 'You said:', message

# Now write some code to tell Winston your favorite food and have him respond 'I love' followed by the food you entered.

# Notice that you just wrote a couple of lines of code that will have a different behavior (what Winston says back to you) depending on the input (the food you give it)! This is a powerful way to handle every possible input that you could be given.
# Here's an idea: since we can input information into a variable using `raw_input`, and we can control the size of shapes using a variable, why don't we combine them?
# That means you can tell Winston what size square to draw and he'll do it!

# Now for a quick detour on data types - we mentioned earlier that variables store values, but one thing that we didn't mention was that there are different types of values!
# You have already seen 2 of those types, namely integers and strings.
# An integer is a whole number, as in `winston.forward(100)`.
# A string is a bunch of characters inside quotes, as in `winston.color("green")`.
# The other common types which we haven't mentioned are floats and booleans.
# A float is a number with a decimal point in it, like '1.5762'
# A boolean is either True or False

# One thing to note is that mathematical operations like `+`,`-`,`*`, and `/` try to give back values which are the same type as the inputs.
# For example Python will evaluate `3/4` into `0` because when the `/` operation is given integers as input, it will return an integer.
# This means that it will "truncate" the decimal `0.75` and just return the integer part `0`.

# If you wanted Python to not truncate, you would perform the division with one of the numbers as a float. Try out the following and compare the results:
print 6/7
print 6.0/7
print 6/7.0
print 6.0/7.0
# As you can see, these are all the same division, but Python interprets them differently based on the type of the data. When you are doing arithmetic where one input is an integer and the other is a float like `6/7.0`, floats take priority over integers and `/` will return a float value instead of an integer.

# Now you can also convert between types like so:
float(1) # becomes 1.0
int(123.63) # becomes 123
str(1) # becomes '1'
int("1342") # becomes 1342
# Note that the last line is problematic because strings can contain any character! Try running
int('THIS STRING DOES NOT HAVE ANY NUMBERS IN IT')
# You should see that Python gives you an error message that basically says that it doesn't know how to convert it into an integer.
# Try the following to get a better idea of how Python converts types:
print int(1.234)
print int('1234')
print float(23)
print str(23)
print int('1a')
# Notice that the last line doesn't print anything because Python doesn't know how to turn 1a into an integer.

# Now that's a lot to digest and it may seem stupid that Python does this, but the main takeaways are that there are different types of data, and that sometimes you can convert between them, and sometimes Python will be upset.

# Lets get back to Winston! So we wanted to tell Winston to draw a square and have him ask what size it should be.
# Let's start with something simpler: Winston should ask how far forward to move. First, note that `raw_input` will give you back a string type, so we need to convert it to an integer before Winston can move forward!
value = raw_input('How far should I move?')
winston.forward(int(value))
# You can see that if you run this and you type an integer in, it will work.
# If you type in something that isn't an integer, the converstion to an integer type will fail and Winston won't move!
###import turtle
###winston = turtle.Turtle()

# Using the same idea, make Winston ask how big of a square to make before he draws it.

# Coolio, now let's expand this so that Winston will also ask what kind of shape to draw!
# To do this, we need to talk about boolean data types and if statements.
# As you learned earlier, a boolean variable is either True or False.
# There are comparisons like `>`, `<`, `>=`, `<=` that will return boolean values for you.
# There are also the `==` and `!=` comparisons, which check if 2 things are equal, and not equal respectively. We use the symbol `==` here because `=` is reserved for setting variable values, and the `!=` because it sort of looks like the &ne; sign.
# Predict what should happen for each of these and then try it out yourself!
print 0 <= 1
print 12.3 > 12.3
print 6 == 12
print 6 != 12
###

# Now here's the cool part - these also work for strings! Strings are compared alphabetically in this case.
'apple' < 'banana' # this is True
'google' > 'googlf' # this is False
'asdf' == 'asdf' # this is True
'asdf' != 'asdf' # this is False
# Python is much faster at alphabetical ordering that a human could ever be. This is what makes searching webpages and sorting Excel columns so fast! We'll explore this some more in later labs.

# Now it's time to introduce the first "control flow" structure: the if statment. By control flow, we mean something that can control which parts of the code are run under different situations. If statements let you run code only when the `if` condition is met. If statements look like this:
if thing:
  print 'thing is True'
# where thing is anything that evaluates to a boolean value. Notice that the code that is indented is what is run when the condition is satisfied. This is the convention that Python uses, and if you have inconsistent indentation, it will complain about it.

# You can also have an `else` portion, which will run only when the `if` condition isn't true:
if variable:
  print 'variable is True'
else:
  print 'variable is False'
# and you can have multiple `elif` portions, if you have more than 2 scenarios. Here's an example of how that could be used in a real program:
money = float(raw_input('How much money do you have?'))
price = 1.50
if money < price:
  print "You don't have enough money!"
elif money == price:
  print "You have exactly enough money!"
else:
  print "You're rich!"
# Try it out and verify that each of the 3 conditions creates the right behavior!

# Now you can use if statements to run different code, i.e. draw different shapes based on a condition. Here's a short example that does something similar:
direction = raw_input('Which direction should I move?')
if direction == 'forward':
  winston.forward(100)
elif direction == 'backward':
  winston.backward(100)
else:
  print "I don't understand that direction!"

# <b>Checkoff Assignment</b>
# Now its your turn - use a `raw_input` so Winston can ask what shape to draw, and another `raw_input` so Winston can ask what size shape to draw and then write an if statement to draw a triangle or square with the inputted size.
# If the shape isn't recognized, then `print` your own error message like the example in the last step.
###import turtle
###winston = turtle.Turtle()

# Great work! Do you feel the power yet? You have just increased your programming vocabulary to include Variables, Input, Output, and If statements.
# These are fundamental building blocks for programming, and we will explore some more next week! Get checked off on your lab and get started on the homework!
