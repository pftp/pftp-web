# Welcome back! Today we're going to cover lists, string manipulation, and HTML!

# Lists are a data type in Python, just like strings or numbers, but the point of a list is to hold multiple values in just one structure! Here's an example:
grocery_list = ['apples', 'strawberries', 'parfait', 'PBR']
for food_item in grocery_list:
  print "Don't forget to buy " + food_item + "!"
# We define a list with [] brackets and a comma-separated list of values. In this case all our list values were strings, but they can be anything: integers, floats, strings, or even other lists! Also, note how we can iterate through our lists extremely easily with the for statement.

# We can also `append` items to our previously defined lists. Here's another way to print the same thing we printed before:
grocery_list = []
grocery_list.append('apples')
grocery_list.append('strawberries')
grocery_list.append('parfait')
grocery_list.append('PBR')
for food_item in grocery_list:
  print "Don't forget to buy " + food_item + "!"

# Sometimes we want to access individual items of a list instead of iterating through every item. We can do this using bracket notation:
grocery_list = ['apples', 'strawberries', 'parfait', 'PBR']
print "First list item: " + grocery_list[1]
print "Zeroth list item: " + grocery_list[0]
print "Third list item: " + grocery_list[3]
print "List length: ", len(grocery_list)
# Wait what? Zeroth item of the list? In Python, lists count their elements starting with zero! So in a list of length 4 (which, btw, we can find using the `len` function), the first item is actually at index 0 and the last item is at index 3 in our list, as you can see from the code above

# We can also pass lists as arguments to functions! Here's a function that sums the elements of a given list:
def get_sum(lst):
  sum = 0
  for item in lst:
    sum = sum + item
  return sum
some_numbers = [3, 5, 2, 3, -8]
other_numbers = [2345, 1234, -1]
print get_sum(some_numbers)
print get_sum(other_numbers)

# A brief interlude on debugging: whenever you don't understand why your program is doing what it's doing, you should drop some `print` statements to figure it out! For example, here's a buggy program that's supposed to compute the product of all the numbers in a given list:
def get_product(lst):
  product = 0
  for item in lst:
    product = product * item
  return product
some_numbers = [3, 5, 2, 3, -8]
other_numbers = [2345, 1234, -1]
print get_product(some_numbers)
print get_product(other_numbers)
# What does this program produce when you run it? Certainly not the product of all the numbers in each list! Let's walk through how to go about debugging this program (even if you already see what's wrong, please bear with me!)

# The first thing we should check is to make sure our lists are getting passed to the function properly. So let's add a print statement like so:
def get_product(lst):
  print "Finding the product of this list: ", lst
  product = 0
  for item in lst:
    product = product * item
  return product
some_numbers = [3, 5, 2, 3, -8]
other_numbers = [2345, 1234, -1]
print get_product(some_numbers)
print get_product(other_numbers)
# Okay so when we run this we get our expected list inputs, so that isn't the problem.

# Next, let's make sure our lists are getting iterated through correctly:
def get_product(lst):
  print "Finding the product of this list: ", lst
  product = 0
  for item in lst:
    print "Multiplying this item: ", item
    product = product * item
  return product
some_numbers = [3, 5, 2, 3, -8]
other_numbers = [2345, 1234, -1]
print get_product(some_numbers)
print get_product(other_numbers)
# Looks like this is also working. Time to check something else.

# Let's look at how our product variable changes each time through our for loop. If all goes well, it should hold a partial product of our list after each iteration. So, for example, when multiplying some_numbers it should be 3, then 15, then 30, then 90, and finally -720. What happens when we run the following?
def get_product(lst):
  print "Finding the product of this list: ", lst
  product = 0
  for item in lst:
    print "Multiplying this item: ", item
    product = product * item
    print "Here's our current product:", product
  return product
some_numbers = [3, 5, 2, 3, -8]
other_numbers = [2345, 1234, -1]
print get_product(some_numbers)
print get_product(other_numbers)
# Okay, what's going on? Our product just stays at 0 the entire time! Figure out why this is happening and fix the bug!

# Coolio, interlude over! Now, write a function that returns the product of only the even elements of a given list. So for some_numbers it should return -16 and for other_numbers it should return 1234. HINT: To check if a number is even, you can write `if num % 2 == 0`, since `%` is the modulus operator which means it gives you the division remainder.
# Then, write a function that returns the product of only the even INDEXED elements of the list. So for some_numbers it should multiply the 0th, 2nd, and 4th elements and return -48 and for other_numbers it should multiply the 0th and 2nd elements and return -2345. HINT: You may want to start your for loop with something like `for i in range(len(lst)):`, which will iterate through all the numbers between 0 and one less than the length of your list. Then, use `lst[i]` to access each item. But only multiply it if the current list index is even!
# Finally, write a function that returns a new list with every item of the initial list doubled. So for some_numbers it should return [6, 10, 4, 6, -16] and for other_numbers it should return [4690, 2468, -2]. HINT: You may want to use the `append` function we taught you earlier!

# Now lets get our graphics skills involved. Import the turtle module and create a new turtle, you can name the turtle whatever you want this time. Then, given a list of shapes, make your turtle draw each shape one by one:
shapes = ['square', 'triangle', 'pentagon', 'hexagon']
for shape in shapes:
  if shape == 'triangle':
    # make your turtle draw a triangle
  elif shape == 'square':
    # make your turtle draw a square
  # etc. for pentagon, hexagon, septagon, and octagon
# You may find it useful to use the 'draw_shape' function we defined in lab 5. You may have to edit it depending on what you named your turtle:
def draw_shape(size, sides):
  for i in range(sides):
    w.forward(size)
    w.left(360./sides)

# Next, we're going to add the ability to specify a color for each of our shapes:
shapes = ['red square', 'blue triangle', 'orange pentagon', 'green hexagon']
# Given this code, we want to our turtle to draw every shape with the specified color. But how do we do that? We could specify every color-shape combination in a giant if statement, but that would be absolute madness!

# Instead, we are going to use string manipulation. String manipulation basically means processing strings to get the information out of them in a form that we can use. In this case, we have to `split` our strings to get their 'color' information and 'shape' information out separately:
for s in shapes:
  shape_pair = s.split(' ')
  if shape_pair[1] == 'triangle':
    # make your turtle draw a triangle of the correct color
  elif shape_pair[1] == 'square':
    # make your turtle draw a square of the correct color
  # etc. for pentagon, hexagon, septagon, and octagon
# Now, when we do `s.split(' ')` it splits our shape string into a LIST of the strings that were previously separated by the space character. So, for example, it splits `"red square"` into `["red", "square"]`. Now, we can access each item of this list separately! Finish off the above code and make your program draw each shape in the proper color. It may be easiest to modify your draw_shape function to do this. Use debugging print statements to help!

# It would be nice if the user of our program didn't actually have to modify the code to draw different shapes. Instead, we'll set up a nice `raw_input` box for them and let them specify the shapes that way! Here's how we'll get user input:
user_input = raw_input('Enter a comma-separated list of shapes in the format: &lt;color&gt; &lt;shape&gt;')
shapes = user_input.split(',')
# Replace the `shapes = ...` line at the top of your program with these two lines.
# Now, you can type something like `yellow septagon,black octagon,purple triangle` as input, and the program will draw multiple shapes!

# <b>Checkoff Assignment</b>
# Finish the shape-drawing program, and also allow the user to specify the size and xy-coordinates of each shape to draw.
# Your user input line should look like this:
user_input = raw_input('Enter a comma-separated list of shapes in the format: &lt;color&gt; &lt;shape&gt; &lt;size&gt; &lt;x-coord&gt; &lt;y-coord&gt;')
# Ex: if the user types `red square 20 -30 60,yellow triangle 100 75 75`, your turtle should draw a red square with side length 20 at (-30, 60) and a yellow triangle with side length 100 at (75, 75)
