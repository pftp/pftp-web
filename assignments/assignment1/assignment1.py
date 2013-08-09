import turtle
import time

# This is Winston, your chelonian (that means turtle) guide to the magic that is python.
winston = turtle.Turtle()

# you can tell Winston to move!
winston.forward(100)
winston.backward(100)

## Give it a try! Make Winston cross the street
# winston.forward(100)

# you can also tell Winston to turn!
winston.left(90)
winston.right(90)

## Tell Winston to spin in a circle clockwise
# winston.right(360)

# with this, you can tell winston to make shapes
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)
winston.right(90)
winston.forward(100)

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
