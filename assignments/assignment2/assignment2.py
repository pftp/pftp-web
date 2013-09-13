# Welcome back! This time, you'll be chatting with Winston and helping him draw shapes!
import turtle
winston = turtle.Turtle()

# If you remember from last lab, Winston can draw a square if you tell him the right things:
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
# But this isn't the easiest code to edit. What if you want to make the square smaller?
# You might have run into this kind of problem while doing the homework -
# It's kind of annoying to edit all 4 'winston.forward(100)' lines to 'winston.forward(60)'
# and it can get pretty tedious when you have a bunch of shapes that you want to change.

# We're big believers in "learning through pain", so we intentionally left out the key
# construct in programming that would allow you to circumvent this problem.
# Well pain no more because it is time! http://www.youtube.com/watch?v=olLxrojmvMg
# Are you ready to feel some more power? Yes? Ok good because programming is chock full of these
# powerful and time-saving ideas and constructs, so you should prepare yourself for the ever increasing power trip
# that you will experience in each lab.

# Introducing variables, an integral part of programming
# that can and will save you lots of time editing values in your code.
# The way variables work is simple: Each variable has a name, and a value which you can set and get. There are several different types of values that Python recognizes:
# Integer (any whole number)
# float (decimal numbers)
# string (anything between quotes, like the colors you use in winston.color)
# boolean (either True or False, we'll discuss these in more depth later)
# You can 'set' the value of a variable named foo using the = sign like so:
foo = 60
bar = 1.5
baz = 'asdf'
nub = True
# Then you can 'get' it's value by just typing it's name. Python will interpret that and replace it with it's value before running the code.
# So wherever you would use a number in your code, you can use 'foo' as well!
foo + 12 # this becomes 72
bar * 4 # this becomes 6.0
winston.right(foo) # turn 60 degrees clockwise

# Now we can make our square code look something like this:
size = 100
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
winston.forward(size)
winston.right(90)
# All that changed was that there is now a variable defined at the top and we use this variable for all the 'winston.forward's.
# This will draw the same square that we originally had, but
# what if we want to change the size of the square now?

# All we have to do is change the value of size, and all the 'winston.forward's will use the new number!
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
# Now that may not seem like much, but consider a regular enneacontagon (a 90-sided polygon) where changing it's size without variables would require changing 90 'winston.forward' lines versus changing just 1 variable if you programmed it like the square above.

# Now with the power of variables under our belts, let's learn how to communicate with Winston!
# Since Winston lives inside the world of Python, he can only talk to us through the 'print' statement.
print 'Hi, {{ current_user.firstname }}!'
# You can

## Now make Winston draw a triangle

# Winston normally drags a pen behind him when he moves, but you can tell him to carry it.
# Hey Winston, stop slacking off and carry the pen
winston.penup()
# now when winston moves, he won't draw anything
winston.forward(100)

# you can use this to tell winston to make separate shapes
# Ok winston you can draw again
winston.pendown()
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)

winston.penup()
winston.forward(100)
winston.pendown()

winston.right(120)
winston.forward(100)
winston.right(120)
winston.forward(100)
winston.right(120)
winston.forward(100)

## now try making a pentagon and a hexagon with some space in between

# cool! your assignment for this week is to make a picture of something

turtle.getscreen()._root.mainloop()
