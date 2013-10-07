# Welcome back! Today we're going to tackle loops! We use loops in Python to make code repeat so we don't have to write it over and over again. There are two types of loops, the "for loop" and the "while loop", and we're going to learn about both today.
# Also I'm tired of typing winston all the time so today we're going to call him "w" for short.
###import Turtle
###w = turtle.Turtle()

# For loops are useful if we already know how many times we want to repeat some action.
# This is an example of a for loop:
for i in range(10):
  print "Here is the current loop variable:"
  print i
# What does this code print when you run it? You should get the numbers 0 through 9 printed out. Now here we've defined our "loop variable" to be called i, and it counts from 0 all the way up to BUT NOT including 10 as our loop runs. We call each time through the loop an "iteration". So this loop will run for 10 iterations and then stop.

# The range function can take 1, 2, or 3 arguments:
# `range(10)` counts from 0 through 9
# `range(2, 8)` counts from 2 through 7
# `range (0, 100, 3)` counts from 0 through 99, counting by 3. We can also use this to count backwards. Try `range (100, 0, -1)` to see how this works!
# Note that we always count from the bottom of our range (0 by default) up to to the top of our range minus one! The reason we do the minus one is that Python loops start at 0 by default, and we want range(10) to mean that our loop actually runs 10 times.

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
# Much simpler! Notice that in this case we didn't use our i variable to actually do anything do anything inside the loop, it just ensures that we do exactly four iterations.

# Loops are a key way we can uphold the DRY, or "Don't Repeat Yourself", principle.
# Write an octagon function using a for loop. Then, try making a shape with 13 sides. Can you do a 100-sided figure?
# Remember the angle to turn after drawing each side is 360 divided by the number of sides.

# Here's a challenge: write a "shape" function that takes two arguments, the size and the number of sides. It should draw a regular polygon with those specifications.
# So `shape(100, 3)` should draw a triangle with side length 3 and `shape(30, 5)` should draw a pentagon with side length 30 and `shape(3, 100)` should draw a 100-sided figure with side length 3.
# HINTS:
# 1. The argument to the "range" function can be a variable too!
# 2. Remember that if we divide an integer by an integer Python will round down automatically without telling us. Try `print 360 / 100` for example. What do you get? We can fix this problem by making 360 a floating point number (a number with a decimal place). Try `print 360.0 / 100`. What do you get now?
# 3. Our shape function was only four lines of code! So if you're writing way more than this you may be doing something inefficient.

# <b>Checkoff Assignment #1</b>
# Now, using the shape function you just wrote, write a for loop to draw every shape from a triangle to a 40-sided figure, all with side length 20. This only took us two more lines of code!
# There's more lab after this, so keep this code around and show it to us at the end along with the other checkoff assignment!

# Now it's time for a brief interlude about the "random" module!
# Here's how we use random:
import random
print random.randint(1, 50)
# This will generate a random number between 1 and 50, inclusive. Try running this code a few times and see what happens. It should print a different number every time! Note that random is another Python module, just like turtle, so we have to import it at the top of our file.

# Okay, now it's time to switch gears and talk about while loops!
# Here's an example of a while loop:
i = 0
while i < 10:
  print "Here is the current value of i:"
  print i
  i = i + 1
# This should print the numbers 0 through 9 when you run it. We can think of a while loop as an if-statement that repeats over and over again until the loop condition is false. Note that we have to keep track of more things here than when we write a for loop: we have to remember to instantiate our i variable to 0 before the loop even starts with `i = 0` and during every iteration of the loop we have to increment the value of i with `i = i + 1`. But, in a sense while loops are more powerful than for loops because it's pretty straightforward to translate any for loop into a while loop but not vice-versa.

# Let's do a random walk with Winston. We'll have Winston move forward 50 units, then turn a random number of degrees, and repeat these actions forever. Actually we want him to stop if he's about to walk of the screen, so we'll make sure he stays inside the middle 400 by 400 box.
# For this you need to know that `w.xcor()` returns Winston's x-position on the screen and `w.ycor()` returns Winston's y-position on the screen. So we want both of these values to stay between -200 and 200. Here's the code:
while w.xcor() > -200 and w.xcor() < 200 and w.ycor() > -200 and w.ycor() < 200:
  w.forward(50)
  w.left(random.randint(0, 359))
# Note that we couldn't possibly have used a for loop for this because we don't know in advance how many steps Winston is going to take before he's outside our boundary box!

# You should also know that we can get out of any loop at any time with the "break" statement.
# So here's another way to write the previous code:
while True:
  if w.xcor() <= -200 or w.xcor() >= 200 or w.ycor() <= -200 or w.ycor() >= 200:
    break
  w.forward(50)
  w.left(random.randint(0, 359))
# Note that a "while True" loop will run forever because the loop condition is literally "True" and that never changes. The only way we can get out of one of these loops is by using the break statement. You can see here that we put an if statement that specifies exactly when Winston is outside our boundary box, and we break out of the loop if he steps outside.
# If you run a "while True" loop and don't break out of it you'll get an infinite loop. This means if you're on our website your browser will freeze, and if you're on the terminal your terminal will hang until you press "Ctrl-C". Try to avoid infinite loops in your programs!

# Let's make a 'guess the password' game. Here's how it works: we continually ask our user for input, and once they guess our password they win! Here's the code:
while True:
  response = raw_input('Guess the password')
  if response == 'Lolociraptorz':
    print 'Congratulations you guessed the password!'
    break
# Now this game is very easy for you if you wrote it, but pretty much impossible for anyone else to win if they can't see the code. So it's kind of a stupid game.

# <b>Checkoff Assignment #2</b>
# Okay, your turn. Your second and final assignment is to write the "guess the number" game. Here's how it works:
# 1. The computer chooses a random number between 1 and 100 for you to guess
# 2. The computer keeps asking the user to guess a number between 1 and 100. If the user guesses too low, the computer prints "too low!" and tells the user to guess again. If the user guesses too high, the computer prints "too high!" and tells the user to guess again. If the user finally guesses the number, then the computer print "congratulations!" and exits.
# HINTS
# 1. Remember that user inputs must be converted from strings to numbers before the computer can use them as numbers! Otherwise you will get weird results.
# 2. Each time this program runs the computer should only generate ONE random number for the user to guess.
