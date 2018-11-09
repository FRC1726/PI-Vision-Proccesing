#!/usr/bin/env bash
killall python

./Server_Vision.py > Vision.log 2> errors.log &
./Ultrasonic.py > Sonic.log 2> errors.log &
