import turtle
winston = turtle.Turtle()
winston.speed(0)

colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink']
def color(i):
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
