from BottleSimulator import BottleSimulator
import time

class map(object):
    def __init__(self):
        ships = [object]

class ship(object):
    def __init__(self,x,y,health = 3):
        self.x = x
        self.y = y
        self.health = health

class player_ship(object):
    def __init__(self,x,y,health = 3):
        self.x = x
        self.y = y
        self.health = health

class laser(object):
    def __init__(self,direction,x,y):
        self.direction = direction
        self.position_x = x
        self.position_y = y

    def move(self):
        position_x += direction

c = BottleSimulator(7, 5, bottle_type="hexagon")
c.draw_bottles()

for i in range(11):
    c.draw_bottle_i(i*3,(255,0,0))
    c.draw_bottle_i(i*3+1,(0,255,0))
    c.draw_bottle_i(i*3+2,(0,0,255))

time.sleep(100)
