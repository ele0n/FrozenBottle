from BottleSimulator import BottleSimulator
import time

c = BottleSimulator(10, 10)
c.draw_bottles()

for i in range(10):
    for j in range(10):
        c.draw_bottle_xy(j,i,(255,0,0))

time.sleep(100)
