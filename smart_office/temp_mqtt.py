# !/usr/bin/python
# coding:utf-8

import time
import Adafruit_DHT
import os

GPIO_PIN = 18

try:
    print('Press Ctrl-C to stop the program')
    while True:
        h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, GPIO_PIN)
        if h is not None and t is not None:
            print('Inside temperature={0:0.1f}C Humidity={1:0.1f}%'.format(t, h))
            os.system('mosquitto_pub -t temperature -m '+str(t)+' -r ')
        else:
            print('Reading failed, read again.')
        time.sleep(30)
except KeyboardInterrupt:
    print('Process stopped')
