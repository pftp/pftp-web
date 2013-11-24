import turtle, sys
import time as tm
winston = turtle.Turtle()
winston.speed(0)
print tm.now()

print new_colors
def color(i):
  colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']
  new_colors = [color[1:] for color in colors]
  return colors[i % len(colors)]

def triangle(size):
  winston.begin_fill()
  for i in [1, 2, 3]:
    winston.forward(size)
    winston.right(120)
  winston.end_fill()

for i in range(300, 1, -5):
  winston.pencolor(color(i))
  winston.fillcolor(color(i))
  triangle(i)

