# Welcome back! This week Winston is going to help you tackle recursion! But first, you should know that:
# `winston.width(10)` will change the thickness of the lines Winston draws.
# `winston.speed(10)` will change Winston's drawing speed.
# `winston.speed(0)` will make Winston's drawing appear instantly, with no animation. This may be useful if you are drawing a compilcated shape and don't want to wait for Winston to draw the whole thing line by line!
# Python will ignore any code after a `#` symbol on any line. This is called a comment and it is useful for reminding ourselves what our code does, as well as for stopping code from executing. So we can write things like
# `winston.forward(10) # this moves winston forward!`
# or
# `#winston.forward(10) haha now winston won't move`
###import turtle
###winston = turtle.Turtle()

# So far in this class, your programs have been limited to a finite number of instructions. Even if you make Winston draw 1,000 lines or more (which you might have done last week with nested functions), he would still finish drawing at some point.
# It turns out you can use functions to make Winston draw forever. How can that work??

# The trick is to define a function that calls itself! Let's make Winston walk in an endless circle:
def endless_circle():
  winston.forward(10)
  winston.left(10)
  endless_circle() # here's the magic!
endless_circle()
# How does this work? Now the last line in our endless_circle definition is `endless_circle()`, so when we reach that line we start the function over again. Then the next time through our function we get to that line and we start the function over again, again. And so on and so on forever!

# Okay, okay Winston enough walking! To make Winston stop walking, you can either:
# 1. Reload the page, or
# 2. Comment out the call to endless_circle() and run the code again. Remember that we use the hash symbol to comment! So replace the last `endless_circle()` with `#endless_circle()` to keep it from running.

# Now it's pretty boring to watch Winston just walk in a circle forever. Let's make him draw a spiral instead!
# In order to do this, we have to add an argument to our function that calls itself:
def spiral(stepsize):
  winston.forward(stepsize)
  winston.left(10)
  spiral(stepsize + .1)
spiral(0)

# So how does this work? Well let's go through instruction by instruction to see. Don't copy-paste the following code, it's just there to illustrate what happens beneath the hood when we run our program.
# We start the whole shebang with `spiral(0)`. This calls our spiral function with stepsize=0, and the following code executes:
winston.forward(0) # These three lines
winston.left(10)   # are what actually happens
spiral(0 + .1)     # when you call spiral(0)
# Notice how these three lines match our definition of spiral exactly, except with stepsize replaced by 0. Hey we just called spiral again with stepsize=.1! This means what really executed was:
winston.forward(0)
winston.left(10)
winston.forward(.1) # These three lines
winston.left(10)    # are what actually happens
spiral(.1 + .1)     # when you call spiral(.1)
# Hey we just called spiral again with stepsize=.2! This means what really executed was:
winston.forward(0)
winston.left(10)
winston.forward(.1)
winston.left(10)
winston.forward(.2) # These three lines
winston.left(10)    # are what actually happens
spiral(.2 + .1)     # when you call spiral(.2)
# And this process will continue on indefinitely.
# So we can see that Winston will walk forward and turn forever, but the amount he walks between turns increases just a tiny bit each time, creating a nice spiral!

# You may have noticed that Winston slows down as he walks. This is not your fault but rather our website lagging.
# You may also have noticed that you get an error in your output: 'RangeError: Maximum call stack size exceeded'. It turns out that Python has a limit on how many nested function calls you can have, which is called the 'maximum call stack size'. So we lied to you: your program won't actually run forever, Python will stop the recursion (and Winston) at some point. Theoretically though your program would run forever if Python could handle it!

# Now it would be nice if we could make Winston draw a spiral and then stop at a specified point instead of going on (almost) forever. So let's add a base case:
def spiral(stepsize):
  if stepsize > 30:
    return
  winston.forward(stepsize)
  winston.left(10)
  spiral(stepsize + .1)
spiral(0)
# Remember that `return` makes our function stop executing right then and there! So now Winston will stop after taking 300 steps, which is convenient.

# Before we move on, play around with the spiral function a little bit! Can you make the spiral wider? Narrower? Counterclockwise instead of clockwise? Can you make Winston spiral inwards to the center instead of outwards from the center? How does our base case have to change to make the spiral fill the entire screen?
# Remember that you can use `winston.speed(0)` if you don't want to wait for Winston to draw everything!

# Now spirals are cool, but fractals are cooler! Last week's triforce3 was an example of a fractal, but we could only go three levels deep because we didn't have recursion. Now that we have recursion, let's see how far we can push the limit:
def triangle(size):
    winston.begin_fill()
    winston.forward(size)
    winston.left(120)
    winston.forward(size)
    winston.left(120)
    winston.forward(size)
    winston.left(120)
    winston.end_fill()
def sierpinski(size):
    if size <= 20:
        triangle(size)
    else:
        sierpinski(size/2)
        winston.forward(size/2)
        sierpinski(size/2)
        winston.backward(size/2)
        winston.left(60)
        winston.forward(size/2)
        winston.right(60)
        sierpinski(size/2)
        winston.left(60)
        winston.backward(size/2)
        winston.right(60)
winston.speed(0)
winston.setposition(-250, -250)
sierpinski(500)

# Holy guacamole how does this one work? If you try to trace through sierpinski the same way we traced through spiral, your head might explode. Instead, just assume that every call to `sierpinski(size/2)` will indeed make a smaller sierpinski and look at one run-through. Between every smaller sierpinski the instructions are actually quite simple, we just move to the position that we need to draw the next sierpinski and then draw it.
# Now notice a very important fact: after each call to sierpinski we reposition Winston so that he's at exactly the same position AND orientation that he started! Therefore, whenever we make a recursive call to sierpinski we know Winston can pick up right where he left off afterwards.
# Try changing the base case size and see what happens. Also, try commenting out `winston.speed(0)` so you can actually watch Winston work! Do you see a pattern in his movements?

# <b>Checkoff Assignment:</b>
# Your turn to make a fractal from scratch! Your assignment this week is to draw <a target="_blank" href="/static/img/tree.png">a tree that looks like this</a>.
# If you're stuck, try making a tree with just two branches to start out with. Then see if you can make each of those branches have branches, and so on. Good luck!
# Here are the specifications:
# Its trunk is 150 units long
# The angle between its branches is 60 degrees
# Each branch is 2/3 as long as its parent branch
# Each branch (and trunk) is 1/5 as wide as it is long
# If a branch is less than 3 units long, draw a leaf instead
# Leaves are green triangles with side length 2

