"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to arrow keys.

"""

import os
import datetime
from turtle import *
from random import randrange
from freegames import square, vector

poops = []
FOOD_RENEW_SECS = 7
FOOD_LOC = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)


def now():
    return datetime.datetime.utcnow()


def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 190 and -200 < head.y < 190


class Food(object):
    def __init__(self, loc=FOOD_LOC, renew_secs=FOOD_RENEW_SECS):
        self.loc = loc
        self.renew_secs = renew_secs
        self.started = now()

    def update(self, loc):
        self.loc = loc
        self.started = now()

    def is_expired(self):
        return (now() - self.started).total_seconds() >= self.renew_secs



food = Food(FOOD_LOC, FOOD_RENEW_SECS)


def get_new_food():
    while True:
        x = randrange(-15, 15) * 10
        y = randrange(-15, 15) * 10
        loc = vector(x, y)
        if inside(loc) and loc not in poops and loc not in snake:
            food.update(loc)
            break





def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def say(msg, game_over=False):
    game_over = ', game over' if game_over else ''
    os.system("say '{}{}' &".format(msg, game_over))

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

    if head == food.loc:
        say("yummy")
        print('Snake:', len(snake))
        get_new_food()

        # do poo
        poo = snake[0].copy()
        poops.append(vector(poo.x, poo.y))

    else:
        snake.pop(0)
        if food.is_expired():
            say('too slow')
            get_new_food()
            if len(snake) > 1:
                snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')
    for body in poops:
        square(body.x, body.y, 9, 'brown')

    square(food.loc.x, food.loc.y, 9, 'green')
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
