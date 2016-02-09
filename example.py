from BottleSimulator import BottleSimulator
import time

c = BottleSimulator(7, 5, bottle_type="hexagon")
c.draw_bottles()
for j in range(256):
    for i in range(11):
        c.draw_bottle_i(i*3,(j,j/2,0))
        c.draw_bottle_i(i*3+1,(0,j,j/2))
        c.draw_bottle_i(i*3+2,(0,j/2,j))

time.sleep(100)
