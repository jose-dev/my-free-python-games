"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to arrow keys.

"""

import os
from turtle import *
from random import randrange
from freegames import square, vector

poops = []
food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)

def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 190 and -200 < head.y < 190

def say(msg, game_over=False):
    game_over = ', game over' if game_over else ''
    os.system("say '{}{}' &".format(msg, game_over))

def get_new_food():
    while True:
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
        if inside(food) and food not in poops and food not in snake:
            break

def move():
    "Move snake forward one segment."
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake or head in poops:
        square(head.x, head.y, 9, 'red')
        update()
        if head in poops:
            say('Yuk, you ate poo', game_over=True)
        elif head in snake:
            say("do not be a cannibal", game_over=True)
        elif not inside(head):
            say("you went too far", game_over=True)
        return

    snake.append(head)

    if head == food:
        say("yummy")
        print('Snake:', len(snake))
        get_new_food()
        #food.x = randrange(-15, 15) * 10
        #food.y = randrange(-15, 15) * 10

        # do poo
        poo = snake[0].copy()
        poops.append(vector(poo.x, poo.y))

    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')
    for body in poops:
        square(body.x, body.y, 9, 'brown')

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, 100)

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move()
done()
