# Welcome back! This week Winston is going to help you tackle recursion! But first, you should know that:
# `winston.width(10)` will change the thickness of the lines Winston draws.
# `winston.speed(10)` will change Winston's drawing speed.
# `winston.speed(0)` will make Winston's drawing appear instantly, with no animation. This may be useful if you are drawing a compilcated shape and don't want to wait for Winston to draw the whole thing line by line!
###import turtle
###winston = turtle.Turtle()

# So far in this class, your programs have been limited to a finite number of instructions. Even if you make Winston draw 1,000 lines or more (which you might have done last week with nested functions), he would still finish drawing at some point.
# It turns out you can use functions to make Winston draw forever. How can that work??

# The trick is to define a function that calls itself! Let's make Winston walk in an endless circle:
def endless_circle():
  winston.forward(10)
  winston.left(10)
  endless_circle()
endless_circle()

# Notice that all the code inside the function is indented, just like for `if` statements.
# If you add this to your code, you will notice that nothing happens. Why? Because this is just a function definition. In order to run or "call" a function, you need to say it's name followed by parentheses, with whatever input values it wants. You have been doing this all along since `winston.forward(100)` is a function call and the input you are giving it is 100!
# Now try adding a call to the `triangle` function you just created and verify that it does in fact draw a triangle! Now this may seem not too revolutionary - in fact we just went from 4 lines to draw a triangle to 6 lines to define a triangle function and call it. Let's take a look at how functions can make things easier.

# Well this triangle is quite boring - no matter what you do, it will draw a triangle in the same size. Fortunately, we can add a function input or "argument" that will let us change this:
def triangle(size):
  winston.forward(size)
  winston.right(120)
  winston.forward(size)
  winston.right(120)
  winston.forward(size)
  winston.right(120)
# This should look familiar to you - it's very similar to what we did with variables and that's because `size` is a variable! The only difference is that now we don't have to explicitly assign a value to `size`, since it will be provided each time `triangle` is called.
# Now add some code to draw 2 trianges of different sizes - remember that now you will need to pass in a value when you call `triangle`. If you don't, you'll get an error like
'TypeError: triangle() takes exactly 1 arguments (0 given)'
# which just means that you need to give triangle a value so that it knows what value to assign to `size`.

# What if we want to fill in the triangle? There are 2 useful commands that we can use here: `winston.begin_fill` and `winston.end_fill`. Anything that Winston draws in between calling these 2 functions will be filled with Winston's current color.
# Now we can use what are called "optional arguments" to fill in the triangle.
def triangle(size, fill=False):
  if fill:
    winston.begin_fill()
  winston.forward(size)
  winston.right(120)
  winston.forward(size)
  winston.right(120)
  winston.forward(size)
  winston.right(120)
  if fill:
    winston.end_fill()
# Notice that we added a fill argument to the `triangle` function, but it looks like we're assigning a value to it! This says that `fill` is an argument to the function, but if you don't give a value for `fill`, it will default to False.
# Try running `triangle(50)`, `triangle(60, False)`, `triangle(70, True)` to get a sense of how the arguments work.

# Now let's try something a little more complicated. What if we want to make one of them fancy radioactive signs?
# Well we have a convenient `triangle` function which we can use, so let's take a shot at it.
def radioactive(size):
  triangle(size, True)
  winston.right(120)
  triangle(size, True)
  winston.right(120)
  triangle(size, True)
  winston.right(120)
# Now this is cool! You can call `radioactive` with different sizes and it will draw the correct size shape! Notice how short the function is - since we defined `triangle` earlier, we can now use it as if it were an instruction that Winston (and Shelby) understand. This is abstraction at work - `triangle` represents a bunch of code to draw a triangle, but all we need to do is just call it by it's name instead of typing `winston.right(120)` a bunch of times.

# Another reason for doing this as opposed to having all 9 `winston.forward`s in `radioactive` is the DRY principle. DRY stands for "Don't repeat yourself" and is one of the most important ideas in programming that allows you to have a lot of control. Writing a function for every block of code that you use a lot is helpful because it not only eliminates the possibility of errors from copying and pasting, but it also allows you to compose functions together like in `radioactive`, leaving you with concise code that is understandable.
# Right now `radioactive` is 7 lines of code, plus the 10 lines for `triangle`. How many lines would `radioactive` be if you didn't use the `triangle` function? The difference is apparent, and it will only get larger as you start composing functions together.

# Now before we continue, take a look at your Homework 2 code and all the `raw_input` lines. It's probaby annoying to have to convert to integers all the time, so we're going to make it easier! Fortunately, there is an `isdigit` function provided by Python which tells you if a string only has numbers in it. Using this, we can write a function `int_input` which will give you back an integer from `raw_input` or `0` if the input wasn't an integer.
def int_input(message):
  value = raw_input(message)
  if value.isdigit():
    return int(value)
  else:
    return 0
# Note that this function "returns" a value, so you can use it like so:
integer_value = int_input("What year were you born in?")
# and the number will be assigned to integer_value!

# It's your turn! Define and call a function to draw a <a target="_blank" href='http://images.wikia.com/zelda/images/2/2a/Black_Triforce.svg'>triforce symbol</a>! You can do this by drawing 3 equal sized triangles or 2 different sized triangles but this is a little tricky because you need to reposition Winston in between `triangle` calls to get the triangles lined up properly. Make sure you can also make it different sizes, and make sure Winston starts and ends at the same position and angle!!
# This is important because when we call the `triforce` function, we want it's behavior to be easy to work with, i.e. Winston starts and ends in the same place.
# Your code should be called using `int_input` so you can ask the user for the size:
size = int_input('How big should I make it?')
triforce(size)


# Cool! Now try writing a `triforce2` function by copying the `triforce` function and replacing `triangle` calls with `triforce` calls that are half the size. If your `triforce` code is correct, calling `triforce2` should give you something like <a target="_blank" href="http://tnellen.com/alt/sierp2.gif">this</a>. This is called a Sierpinski triangle and it is a type of fractal, which we will discuss next week.

# <b>Checkoff Assignment:</b>
# Now try writing a `triforce3` function by copying the `triforce2` code and replacing `triforce` with `triforce2`. You should get a pretty rad drawing using way less lines of code than if you were to write that line by line!
