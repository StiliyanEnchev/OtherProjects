import turtle
import heroes

timmy_the_turtle = turtle.Turtle()

for i in range(4):
    timmy_the_turtle.forward(100)
    timmy_the_turtle.right(90)
    timmy_the_turtle.forward(100)
    timmy_the_turtle.forward(100)

timmy_the_turtle.circle(100)
timmy_the_turtle.left(90)
timmy_the_turtle.forward(200)
timmy_the_turtle.backward(200)

timmy_the_turtle.left(90)
timmy_the_turtle.circle(100)



screen = turtle.Screen()
screen.exitonclick()

print (heroes.gen())