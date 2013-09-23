# Oh hey you're back! Winston is joining us and he also brought his friend Shelby!
# Say hi to Shelby! She'll be helping us learn about abstraction this week.
###import turtle
###winston = turtle.Turtle()
###shelby = turtle.Turtle()

# You can control Winston and Shelby separately! Try making Winston and Shelby draw a square each.
# It's kind of hard to tell Winston and Shelby apart, so make them different colors before they start drawing too.

# Cool! Now that we have that down, let's take a look at the motivation for all this abstraction.
# Open up your Homework 1 and Homework 2 code in separate tabs and count how many lines they are. Is it 100 lines? 200 lines?
# How many of those lines are `winston.forward`s? Probably a lot of them. If you drew a bunch of squares, you'll have a lot of `winston.right`s or `winston.left`s.

# We can use functions to "unduplicate" a lot of this code, just like we used variables to "unduplicate" a lot of numbers!
# Let's take a look at a function that will draw a triangle.
def triangle():
  winston.forward(100)
  winston.right(120)
  winston.forward(100)
  winston.right(120)
  winston.forward(100)
  winston.right(120)
# Notice that all the code inside the function is indented, just like for `if` statements.
# If you add this to your code, you will notice that nothing happens. Why? Because this is just a <b>function definition</b>. In order to run or "call" a function, you need to say it's name followed by parentheses, with whatever input values it wants. You have been doing this all along since `winston.forward(100)` is a function call and the input you are giving it is 100!
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


# It's your turn! Define and call a function to draw a <a target="_blank" href='http://images.wikia.com/zelda/images/2/2a/Black_Triforce.svg'>triforce symbol</a>! You can do this by drawing 3 equal sized triangles or 2 different sized triangles but this is a little tricky because you need to reposition Winston in between `triangle` calls to get the triangles lined up properly. Make sure you can also make it different sizes, and make sure Winston starts and ends at the same position and angle!!
# This is important because when we call the `triforce` function, we want it's behavior to be easy to work with, i.e. Winston starts and ends in the same place.

# <b>Checkoff Assignment:</b>
# Cool! Now try writing a `triforce2` function by copying the `triforce` function and replacing `triangle(size, True)` with `triforce(s/2)`. If your `triforce` code is correct, calling `triforce2` should give you something like <a target="_blank" href="http://tnellen.com/alt/sierp2.gif">this</a>. This is called a Sierpinski triangle and it is a type of fractal, which we will discuss next week. If you're feeling particularly adventurous, try writing a `triforce3` function by copying the `triforce2` code and replacing `triforce` with `triforce2`. You should get a pretty rad drawing using way less lines of code than if you were to write that line by line!
