import turtle
win = turtle.Screen()
pen = turtle.Turtle()
pen.speed(0)
color = ('red', 'yellow', 'black', 'green', 'blue')
rad = 50
size = 1
# win.tracer(100)
while 1:
    for i, pos in enumerate([[-100, -rad], [-50, -rad-50], [0, -rad], [50, -rad-50], [100, -rad]]):
        pen.hideturtle()
        pen.up()
        pen.setpos(pos)
        pen.showturtle()
        pen.down()
        pen.color(color[i])
        pen.pensize(size)
        pen.circle(rad)
    rad += 1
