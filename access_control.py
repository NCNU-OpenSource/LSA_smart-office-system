from datetime import datetime
from datetime import date
import sqlite3
from sqlite3 import Error
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

# Servo Motor setting
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
servo1 = GPIO.PWM(7, 50)  # Note 7 is pin, 50 = 50Hz pulse


def dooropen(servo1):
    # start PWM running, but with value of 0 (pulse off)
    servo1.start(0)

    # Turn back to 90 degrees
    servo1.ChangeDutyCycle(7)
    time.sleep(3)

    # turn back to 0 degrees
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

    # Clean things up at the end
    servo1.stop()


# RFID read card
reader = SimpleMFRC522()
print("Now place your tag to Read")
cardid, text = reader.read()

# Variables
today = date.today()
now = datetime.now()
keyid = str(today)+"_"+str(cardid)

# Connect database
conn = sqlite3.connect('/home/pi/database/company_record.db')
cursor = conn.cursor()

# Create new table if not exist
sqlstr = 'CREATE TABLE IF NOT EXISTS record ("keyid" TEXT PRIMARY KEY NOT NULL, "date" DATE, "cardid" TEXT, "name" TEXT, "starttime" DATETIME, "endtime" DATETIME)'
cursor.execute(sqlstr)

# Check card ID in staff list
sqlstr = 'SELECT * FROM stafflist WHERE cardid=?'
cursor.execute(sqlstr, (cardid,))
row = cursor.fetchone()
if not row == None:
    # Insert data if not exist
    sqlstr = 'INSERT OR IGNORE INTO record VALUES(?, ?, ?, ?, ?, ?);'
    cursor.execute(sqlstr, (keyid, today, cardid, row[1], now, now))

    # Update endtime
    sqlstr = 'UPDATE record SET endtime=? WHERE keyid=?;'
    cursor.execute(sqlstr, (now, keyid))

    print("Login successfully")
    dooropen(servo1)
else:
    print("Login failed")

GPIO.cleanup()
conn.commit()
conn.close()
