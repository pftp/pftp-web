#Welcome to Lab 1! We are going to learn some turtle graphics today. Hit the 'Next' button to get started.

# This is Winston, your guide to the magic that is Python.
# Don't worry about what `import` or `turtle.Turtle()` means - we will get into that later. All that matters is that we have a turtle and his name is Winston. He will listen to your instructions and execute them in order with no mistakes because he is just that good.
###import turtle
###winston = turtle.Turtle()

# You can call Winston by his name and tell him to move! Try adding a line at the end that says `winston.forward(100)`. This tells Winston to move 100 units in the direction he's facing. Hit the 'Run It!' button when you're done to see Winston in action.

# Now try bringing Winston back to where he started with `winston.backward()` (You still need to supply a number between the parentheses so Winston knows how far to go.

# Winston can even change directions! Try telling Winston to turn right by adding a line at the end that says `winston.right(90)`.

# Try making Winston spin in a circle counter-clockwise. (Hint: Winston will have to turn left and he only understands angles in degrees.

# Now Winston is pretty smart for a turtle, and using just these commands, you can tell him to draw shapes. Try adding these lines at the end:
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)

# Now it's your turn! Make Winston draw a triangle. You can edit or delete the lines from the previous step to do this.

# Cool! Now normally Winston drags a pen behind him when he moves, and this leaves the lines that you see. You can tell Winston to stop slacking off and carry the pen if you don't want him to draw: `winston.penup()`. Try adding this line and then make Winston move. You should see that there is no line behind him as he moves this time!

# You can use this to make separate shapes! Just tell Winston to put his pen back down and draw a shape, and then pick it up while he moves to a different spot to start the next shape. Try adding these lines to see it:
winston.pendown()
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.penup()
winston.forward(200)
winston.pendown()
winston.right(120)
winston.forward(100)
winston.right(120)
winston.forward(100)
winston.right(120)
winston.forward(100)

# Now you try making a pentagon inside of a hexagon.

# Winston also has one of those giant packs of crayons, so you can tell him to change the color he draws too: `winston.color("green")`. He will understand the following list of colors:
aliceblue
antiquewhite
aqua
aquamarine
azure
beige
bisque
black
blanchedalmond
blue
blueviolet
brown
burlywood
cadetblue
chartreuse
chocolate
coral
cornflowerblue
cornsilk
crimson
cyan
darkblue
darkcyan
darkgoldenrod
darkgray
darkgreen
darkgrey
darkkhaki
darkmagenta
darkolivegreen
darkorange
darkorchid
darkred
darksalmon
darkseagreen
darkslateblue
darkslategray
darkslategrey
darkturquoise
darkviolet
deeppink
deepskyblue
dimgray
dimgrey
dodgerblue
firebrick
floralwhite
forestgreen
fuchsia
gainsboro
ghostwhite
gold
goldenrod
gray
green
greenyellow
grey
honeydew
hotpink
indianred
indigo
ivory
khaki
lavender
lavenderblush
lawngreen
lemonchiffon
lightblue
lightcoral
lightcyan
lightgoldenrodyellow
lightgray
lightgreen
lightgrey
lightpink
lightsalmon
lightseagreen
lightskyblue
lightslategray
lightslategrey
lightsteelblue
lightyellow
lime
limegreen
linen
magenta
maroon
mediumaquamarine
mediumblue
mediumorchid
mediumpurple
mediumseagreen
mediumslateblue
mediumspringgreen
mediumturquoise
mediumvioletred
midnightblue
mintcream
mistyrose
moccasin
navajowhite
navy
oldlace
olive
olivedrab
orange
orangered
orchid
palegoldenrod
palegreen
paleturquoise
palevioletred
papayawhip
peachpuff
peru
pink
plum
powderblue
purple
red
rosybrown
royalblue
saddlebrown
salmon
sandybrown
seagreen
seashell
sienna
silver
skyblue
slateblue
slategray
slategrey
snow
springgreen
steelblue
tan
teal
thistle
tomato
turquoise
violet
wheat
white
whitesmoke
yellow
yellowgreen

# Awesome! Now your assignment for this week is to make a picture of something cool
