from BottleSimulator import BottleSimulator
import time

c = BottleSimulator(7,5,4)
for i in range(11):
    c.send(i*3,255,0,0)
    c.send(i*3+1,0,255,0)
    c.send(i*3+2,0,0,255)
time.sleep(100)
