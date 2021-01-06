# write table to csv

import sqlite3
import csv

# Connect database
conn = sqlite3.connect('/home/pi/database/company_record.db')
# conn = sqlite3.connect('company_record.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM record')
with open('/home/pi/database/record.csv', 'w', newline='') as out_csv_file:
    # with open('output.csv', 'w', newline='') as out_csv_file:
    csv_out = csv.writer(out_csv_file)
    # write header
    # csv_out.writerow([d[0] for d in cursor.description])
    # write data
    for result in cursor:
        print(result)
        csv_out.writerow(result)
conn.close()
