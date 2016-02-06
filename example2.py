from BottleSimulator import BottleSimulator
import time

c = BottleSimulator(10, 10)

for j in range(100):
    c = BottleSimulator(1+j, 1+j)
    c.draw_bottles()
    time.sleep(0.3)

time.sleep(500)
