# !/usr/bin/python
# coding:utf-8

import time
import Adafruit_DHT
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

A1A = 18
A1B = 16
TEMP_PIN = 18  # pi board pin 12
GPIO.setup(A1A, GPIO.OUT)
GPIO.setup(A1B, GPIO.OUT)                                        
GPIO.output(A1A, GPIO.LOW)
GPIO.output(A1B, GPIO.LOW)
while True:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    A1A = 18
    A1B = 16
    TEMP_PIN = 18  # pi board pin 12
    GPIO.setup(A1A, GPIO.OUT)
    GPIO.setup(A1B, GPIO.OUT)        
    try:
        h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, TEMP_PIN)
        if h is not None and t is not None:
            print('Temperature={0:0.1f}C Humidity={1:0.1f}%'.format(t, h))
            if t > 20.0:
                print("HOT")
                GPIO.output(A1A, GPIO.LOW)
                GPIO.output(A1B, GPIO.HIGH)
            else:
                GPIO.output(A1A, GPIO.LOW)
                GPIO.output(A1B, GPIO.LOW)
        else:
            print('Reading failed, read again.')
        time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()
