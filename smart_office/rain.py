#!/usr/bin/env python

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

RAIN_PIN = 8

GPIO.setup(RAIN_PIN, GPIO.IN)

# state = GPIO.input(RAIN_PIN)
# state_2 = GPIO.input(RAIN_PIN_2)

# print(state)
# print(state_2)

#state = GPIO.input(RAIN_PIN)

try:
    print('Press Ctrl-C to stop the program')
    while True:
        os.system('mosquitto_pub -t rain -m '+str(GPIO.input(RAIN_PIN))+' -r ')
        if (GPIO.input(RAIN_PIN) == 0):
            print("Water detected!")
        else:
            print("Water not detected")
        time.sleep(30)

except KeyboardInterrupt:
    print('Process stopped')
