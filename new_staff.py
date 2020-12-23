
import sqlite3
from sqlite3 import Error
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Input name
name = input('Input your name:')

# Connect database
conn = sqlite3.connect('/home/pi/database/company_record.db')
cursor = conn.cursor()

# Check and create table
sqlstr = 'CREATE TABLE IF NOT EXISTS stafflist ("staffid" INTEGER PRIMARY KEY AUTOINCREMENT, "name" TEXT, "cardid" TEXT UNIQUE)'
cursor.execute(sqlstr)

# Insert data if not exist
sqlstr = 'INSERT OR IGNORE INTO stafflist VALUES(?, ?, ?);'
cursor.execute(sqlstr, (1, "admin", "00000000"))

# RFID Reader and Check RFID card used
reader = SimpleMFRC522()
try:
    while True:
        print("Now place your tag to write")
        cardid, text = reader.read()
        sqlstr = 'SELECT * FROM stafflist WHERE cardid=?'
        cursor.execute(sqlstr, (cardid,))
        row = cursor.fetchone()
        print(row)
        if not row == None:
            print("ERROR: RFID card used, please try another RFID card")
            continue
        else:
            break

finally:
    GPIO.cleanup()


# Insert data
sqlstr = 'INSERT INTO stafflist (name,cardid) VALUES (?, ?);'
cursor.execute(sqlstr, (name, cardid))

print("Data added successfully")

conn.commit()
conn.close()
