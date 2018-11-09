#!/usr/bin/env python

#Libraries
import RPi.GPIO as GPIO
import time

import threading
from networktables import NetworkTables
from Queue import Queue

cond = threading.Condition()
notified = [False]

queueSize = 10
window = Queue(queueSize)
spikeThreshold = 50

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.17.26.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
 
with cond:
    print("Waiting for network tables")
    if not notified[0]:
        cond.wait()
        
print("Let there be network tables")

table = NetworkTables.getTable('SmartDashboard')
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
     
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
  
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        sum = 0
        distPrevious = 0
        while True:
            if(not window.full()):
                dist = distance()
                if(abs(distPrevious - dist) < spikeThreshold):
                    window.put(dist)
                    sum += dist
                    #print ("Measured Distance = %.1f cm" % dist)
                    
                distPrevious = dist;
                time.sleep(.05)
                
            elif(window.full()):
                table.putNumber('Distance', sum / queueSize)
                sum -= window.get()
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        # Catch all other exceptions
    except Exception as e:
        print("an unknown error occured:")
        print(e)
        GPIO.cleanup()
