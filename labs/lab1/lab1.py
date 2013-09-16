import turtle
import time

#Wrapper class to display messages and pause between steps
class Turtle(object):
  def __init__(self):
    turtle.bgcolor("black")
    self.turtle = turtle.Turtle()
    self.turtle.pencolor("white")

  def forward(self, amt):
    self.turtle.forward(amt)
    time.sleep(3)

  def backward(self, amt):
    self.turtle.backward(amt)
    time.sleep(3)

  def left(self, amt):
    self.turtle.left(amt)
    time.sleep(3)

  def right(self, amt):
    self.turtle.right(amt)
    time.sleep(3)

  def say(self, msg):
    self.turtle.write(msg)
    time.sleep(3)


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

# by combining these instructions, you can tell winston to make shapes
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
