import RPi.GPIO as GPIO
import time
import os
import subprocess
from subprocess import STDOUT, check_output

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

A1A = 18
A1B = 16

GPIO.setup(A1A, GPIO.OUT)
GPIO.setup(A1B, GPIO.OUT)


def fan(d):
    d = str(d)
    d = d.strip("b")
    d = d.strip("'")
    d = d.strip("n")
    d = d.strip("\\")
    if d == "O":
        GPIO.output(A1A, GPIO.LOW)
        GPIO.output(A1B, GPIO.HIGH)
    elif d == "F" :
        GPIO.output(A1A, GPIO.LOW)
        GPIO.output(A1B, GPIO.LOW)

with subprocess.Popen("mosquitto_sub -h [IP of broker that you subscribe control signal] -t switch",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:    
    for line in p.stdout:
        fan(line) 
        
