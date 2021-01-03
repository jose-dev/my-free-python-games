"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to arrow keys.

"""

import os
import random
import datetime
from turtle import *
from random import randrange
from freegames import square, vector

#poops = []
POO_EXPIRE_SECS = 60
FOOD_EXPIRE_SECS = 7
FOOD_LOC = vector(0, 0)
#snake = [vector(10, 0)]
aim = vector(0, -10)


def now():
    return datetime.datetime.utcnow()


class Item(object):
    def __init__(self, loc, expiry_secs, color):
        self.loc = loc
        self.expiry_secs = expiry_secs
        self.started = now()
        self.color = color

    def is_expired(self):
        return (now() - self.started).total_seconds() >= self.expiry_secs

    def draw(self):
        square(self.loc.x, self.loc.y, 9, self.color)


class Food(Item):
    def __init__(self, loc=FOOD_LOC, expiry_secs=FOOD_EXPIRE_SECS):
        super().__init__(loc, expiry_secs, 'green')

    def update(self, loc):
        self.loc = loc
        self.started = now()
        self.set_color()

    def set_color(self):
        color = random.choices(population=['green', 'cyan', 'yellow'], weights=[0.6, 0.2, 0.2], k=1)[0]
        self.color = color


class Poo(Item):
    def __init__(self, loc, expiry_secs=POO_EXPIRE_SECS):
        super().__init__(loc, expiry_secs, 'brown')


class Poops(object):
    def __init__(self):
        self.items = []

    def add(self, loc):
        self.items.append(Poo(loc))

    def draw(self):
        items = []
        for item in self.items:
            if not item.is_expired():
                square(item.loc.x, item.loc.y, 9, item.color)
                items.append(item)
        self.items = items


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


class SnakeSkin(object):
    def __init__(self, body):
        self.body = body
        self.color = 'grey'
        self.started = now()
        self.expiry_secs = 20

    def is_expired(self):
        return (now() - self.started).total_seconds() >= self.expiry_secs

    def draw(self):
        if self.is_expired():
            self.body = []
        else:
            for body in self.body:
                square(body.x, body.y, 9, self.color)


class PoopingSnakeController(object):
    def __init__(self):
        self.food = Food()
        self.snake = Snake()
        self.poops = Poops()
        self.snake_skin = SnakeSkin([])
        self.set_speed()
        self.last_shed = now()
        self.shed_cycle_secs = 30

    def is_shedding_time(self):
        if (now() - self.last_shed).total_seconds() >= self.shed_cycle_secs:
            self.last_shed = now()
            return True
        return False

    def get_new_food(self):
        while True:
            x = randrange(-15, 15) * 10
            y = randrange(-15, 15) * 10
            loc = vector(x, y)
            if self.is_valid_move(loc):
                self.food.update(loc)
                break

    def set_speed(self):
        mode = self.food_energy()
        speed = 100
        if mode == 'fast':
            speed = 70
        elif mode == 'slow':
            speed = 140
        self.speed = speed

    def ate_food(self):
        it_did = self.snake.head() == self.food.loc
        if it_did:
            self.set_speed()
        return it_did

    def food_energy(self):
        energy = {'green': 'default',
                  'yellow': 'slow',
                  'cyan': 'fast'}
        return energy.get(self.food.color, 'default')

    def inside(self, loc):
        "Return True if head inside boundaries."
        return -200 < loc.x < 190 and -200 < loc.y < 190

    def is_valid_move(self, loc):
        return self.inside(loc) and loc not in [r.loc for r in self.poops.items] \
               and loc not in self.snake.body and loc not in self.snake_skin.body

    def is_invalid_move(self, loc):
        return not self.inside(loc) or loc in self.snake.body \
               or loc in [r.loc for r in self.poops.items] or loc in self.snake_skin.body

    def invalid_move_message(self, loc):
        if loc in [r.loc for r in self.poops.items]:
            return 'Yuk, you ate poo'
        elif loc in self.snake.body:
            return "do not be a cannibal"
        elif loc in self.snake_skin.body:
            return "Yuk, you ate your own skin"
        elif not self.inside(loc):
            return "you went too far"

    def draw(self):
        if self.is_shedding_time():
            self.snake_skin = SnakeSkin(self.snake.body.copy())
        self.snake.draw()
        self.poops.draw()
        self.food.draw()
        self.snake_skin.draw()




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

    ctl.draw()

    update()
    ontimer(move, ctl.speed)

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
