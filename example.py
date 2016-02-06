from BottleSimulator import BottleSimulator
import time

c = BottleSimulator(7, 5, bottle_type="hexagon")
c.draw_bottles()

for i in range(11):
    c.draw_bottle_i(i*3,(255,0,0))
    c.draw_bottle_i(i*3+1,(0,255,0))
    c.draw_bottle_i(i*3+2,(0,0,255))

time.sleep(100)
