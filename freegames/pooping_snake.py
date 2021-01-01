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

#poops = []
FOOD_RENEW_SECS = 7
FOOD_LOC = vector(0, 0)
#snake = [vector(10, 0)]
aim = vector(0, -10)


def now():
    return datetime.datetime.utcnow()




class Item(object):
    def __init__(self, loc, expiry_secs):
        self.loc = loc
        self.expiry_secs = expiry_secs
        self.started = now()

    def update(self, loc):
        self.loc = loc
        self.started = now()

    def is_expired(self):
        return (now() - self.started).total_seconds() >= self.expiry_secs


class Food(Item):
    def __init__(self, loc=FOOD_LOC, expiry_secs=FOOD_RENEW_SECS):
        super(Food, self).__init__(loc, expiry_secs)


class Snake(object):
    def __init__(self):
        self.body = [vector(10, 0)]

    def head(self):
        return self.body[-1].copy()

    def tail(self):
        return self.body[0].copy()

    def length(self):
        return len(self.body)

    def append(self, v):
        self.body.append(v)

    def pop(self):
        self.body.pop(0)


class PoopingSnakeController(object):
    def __init__(self):
        self.food = Food()
        self.snake = Snake()
        self.poops = []

    def get_new_food(self):
        while True:
            x = randrange(-15, 15) * 10
            y = randrange(-15, 15) * 10
            loc = vector(x, y)
            if self.inside(loc) and loc not in self.poops and loc not in self.snake.body:
                self.food.update(loc)
                break

    def ate_food(self):
        return self.snake.head() == self.food.loc

    def inside(self, loc):
        "Return True if head inside boundaries."
        return -200 < loc.x < 190 and -200 < loc.y < 190



ctl = PoopingSnakeController()



def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def say(msg, game_over=False):
    game_over = ', game over' if game_over else ''
    os.system("say '{}{}' &".format(msg, game_over))

def move():
    "Move snake forward one segment."
    head = ctl.snake.head()
    head.move(aim)

    if not ctl.inside(head) or head in ctl.snake.body or head in ctl.poops:
        square(head.x, head.y, 9, 'red')
        update()
        if head in ctl.poops:
            say('Yuk, you ate poo', game_over=True)
        elif head in ctl.snake.body:
            say("do not be a cannibal", game_over=True)
        elif not ctl.inside(head):
            say("you went too far", game_over=True)
        return

    ctl.snake.append(head)

    if ctl.ate_food():
        say("yummy")
        print('Snake:', ctl.snake.length())
        ctl.get_new_food()

        # do poo
        poo = ctl.snake.tail()
        ctl.poops.append(vector(poo.x, poo.y))

    else:
        ctl.snake.pop()
        if ctl.food.is_expired():
            say('too slow')
            ctl.get_new_food()
            if ctl.snake.length() > 1:
                ctl.snake.pop(0)

    clear()

    for body in ctl.snake.body:
        square(body.x, body.y, 9, 'black')
    for body in ctl.poops:
        square(body.x, body.y, 9, 'brown')

    square(ctl.food.loc.x, ctl.food.loc.y, 9, 'green')
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
