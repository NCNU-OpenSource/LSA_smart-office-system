# !/usr/bin/python
# coding:utf-8

import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import subprocess
import os
from subprocess import STDOUT, check_output


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

A1A = 18
A1B = 16
TEMP_PIN = 18  # pi board pin 12

GPIO.setup(A1A, GPIO.OUT)
GPIO.setup(A1B, GPIO.OUT)                                        
GPIO.output(A1A, GPIO.LOW)
GPIO.output(A1B, GPIO.LOW)

def auto(mes):
    if mes == "O":
        subprocess.Popen("python temp_control_fan_auto.py", shell=True)
    elif mes == "F":
        os.system('pkill -f temp_control_fan_auto.py')
with subprocess.Popen("mosquitto_sub -h [IP of broker that you subscribe control signal] -t auto_switch",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
    for line in p.stdout:
        mes = str(line)
        mes = mes.strip("b")
        mes = mes.strip("'")
        mes = mes.strip("n")
        mes = mes.strip("\\")
        print(mes)
        auto(mes)
