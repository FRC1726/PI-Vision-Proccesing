#!/usr/bin/env python

from pixy import *
from ctypes import *
from time import sleep

import threading
from networktables import NetworkTables

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.17.26.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()
        
print("Let there be network tables")

table = NetworkTables.getTable('SmartDashboard')


class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks = BlockArray(100)
CENTER = 159
RANGE = 7

print("Let there be pixy")
pixy_init()

while True:
    NumBlocks = pixy_get_blocks(100, blocks)

    if NumBlocks > 0:
        area = 0
        for i in range(0, NumBlocks):
            currentArea = blocks[i].width * blocks[i].height
            if currentArea > area:
                largestBlock = i
                area = currentArea
                
        currentX = blocks[largestBlock].x
        offset = currentX - CENTER
        table.putNumber('X position', offset)
        table.putBoolean('Blocks Detected', True)
        
        
        if abs(offset) <= RANGE:
            print("center")
        elif offset < 0:
            print("left")
        elif offset > 0:
            print("right")
    else:
        print("No Blocks Detected")
        table.putBoolean('Blocks Detected', False)
    
    sleep(1)
          
    
        