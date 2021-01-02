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
        self.color = 'green'

    def draw(self):
        square(self.loc.x, self.loc.y, 9, self.color)


class Poops(object):
    def __init__(self):
        self.items = []
        self.color = 'brown'

    def add(self, loc):
        self.items.append(loc)

    def draw(self):
        for body in self.items:
            square(body.x, body.y, 9, self.color)


class Snake(object):
    def __init__(self):
        self.body = [vector(10, 0)]
        self.color = 'black'

    def head(self):
        return self.body[-1].copy()

    def tail(self):
        return self.body[0].copy()

    def length(self):
        return len(self.body)

    def grow(self, v):
        self.body.append(v)

    def shrink(self):
        self.body.pop(0)

    def move(self):
        self.shrink()

    def poop(self):
        self.shrink()

    def draw(self):
        for body in self.body:
            square(body.x, body.y, 9, self.color)



class PoopingSnakeController(object):
    def __init__(self):
        self.food = Food()
        self.snake = Snake()
        self.poops = Poops()

    def get_new_food(self):
        while True:
            x = randrange(-15, 15) * 10
            y = randrange(-15, 15) * 10
            loc = vector(x, y)
            if self.inside(loc) and loc not in self.poops.items and loc not in self.snake.body:
                self.food.update(loc)
                break

    def ate_food(self):
        return self.snake.head() == self.food.loc

    def inside(self, loc):
        "Return True if head inside boundaries."
        return -200 < loc.x < 190 and -200 < loc.y < 190

    def is_invalid_move(self, loc):
        return not self.inside(loc) or loc in self.snake.body or loc in self.poops.items

    def invalid_move_message(self, loc):
        if loc in self.poops.items:
            return 'Yuk, you ate poo'
        elif loc in self.snake.body:
            return "do not be a cannibal"
        elif not self.inside(loc):
            return "you went too far"



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

    if ctl.is_invalid_move(head):
        square(head.x, head.y, 9, 'red')
        update()
        say(ctl.invalid_move_message(head), game_over=True)
        return

    ctl.snake.grow(head)

    if ctl.ate_food():
        say("yummy")
        print('Snake:', ctl.snake.length())
        ctl.get_new_food()

        # do poo
        ctl.poops.add(ctl.snake.tail())

    else:
        ctl.snake.move()
        if ctl.food.is_expired():
            say('too slow')
            ctl.get_new_food()
            if ctl.snake.length() > 1:
                ctl.poops.add(ctl.snake.tail())
                ctl.snake.shrink()

    clear()

    ctl.snake.draw()
    ctl.poops.draw()
    ctl.food.draw()

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
