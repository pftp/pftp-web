# Welcome back! Today we're going to tackle loops! We use loops in Python to make
# code repeat so we don't have to write it over and over again. There are two types
# of loops, the "for loop" and the "while loop", and we're going to learn about
# both today. Also I'm tired of typing winston all the time so today we're going
# to call him "w" for short.
### import Turtle
### w = turtle.Turtle()

# For loops are useful if we already know how many times we want to repeat some action.
# This is an example of a for loop:
for i in range(10):
  print "Here is the current loop variable:"
  print i
# What does this code print when you run it? You should get the numbers 0 through 9
# printed out. Now here we've defined our "loop variable" to be called i, and it
# counts from 0 all the way up to BUT NOT including 10 as our loop runs. We call each
# time through the loop an "iteration". So this loop will run for 10 iterations and then stop.

# The range function can take 1, 2, or 3 arguments:
# `range(10)` counts from 0 through 9
# `range(2, 8)` counts from 2 through 7
# `range (0, 100, 3)` counts from 0 through 99, counting by 3
# Note that we always count from the bottom of our range (0 by default) up to to the
# top of our range minus one! The reason we do the minus one is that Python loops start
# at 0 by default, and we want range(10) to mean that our loop actually runs 10 times.

# Remember our code telling Winston to draw a square?
def square(size):
  w.forward(size)
  w.left(90)
  w.forward(size)
  w.left(90)
  w.forward(size)
  w.left(90)
  w.forward(size)
  w.left(90)
# How can we shorten this code with a for loop?

# Note that we just repeated the exact same code four times inside our square function.
# So we'll just stick that code inside a for loop and make sure the loop runs four times:
def square(size):
  for i in range(4):
    w.forward(size)
    w.left(90)
# Much simpler! Notice that in this case we didn't use our i variable to actually do anything
# do anything inside the loop, it just ensures that we do exactly four iterations.

# Loops are a key way we can uphold the DRY, or "Don't Repeat Yourself", principle.
# Write an octagon function using a for loop. Then, try making a shape with 13 sides.
# Can you do a 100-sided figure? Remember the angle to turn after drawing each side
# is 360 divided by the number of sides.

# Here's a challenge: write a "shape" function that takes two arguments, the size
# and the number of sides. So `shape(100, 3)` should draw a triangle with side length
# 3 and `shape(30, 5)` should draw a pentagon with side length 30 and `shape(3, 100)`
# should draw a 100-sided figure with side length 3.
#
# HINTS:
# 1. The argument to the "range" function can be a variable too!
#
# 2. Remember that if we divide an integer by an integer Python will round down
# automatically without telling us. Try `print 360 / 100` for example. What do
# you get? We can fix this problem by making 360 a floating point number (a number
# with a decimal place). Try `print 360.0 / 100`. What do you get now?
#
# 3. Our shape function was only four lines of code! So if you're writing way more
# than this you may be doing something inefficient.

# Now, using the shape function you just wrote, write a for loop to draw every shape
# from a triangle to a 40-sided figure, all with side length 20. This only took us
# two more lines of code!


# Okay, now it's time to switch gears and talk about while loops!
