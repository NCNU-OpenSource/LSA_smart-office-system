#!/usr/bin/python
# coding=utf-8
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3


def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        path, scopes)
    return gspread.authorize(credentials)


auth_json_path = '/home/pi/smart_office/auth.json'  # 由剛剛建立出的憑證，放置相同目錄以供引入
gss_scopes = ['https://spreadsheets.google.com/feeds']  # 我們想要取用的範圍
gss_client = auth_gss_client(auth_json_path, gss_scopes)  # 呼叫我們的函式

# 從剛剛建立的sheet，把網址中 https://docs.google.com/spreadsheets/d/〔key〕/edit 的 〔key〕的值代入
spreadsheet_key_path = 'KEY'

# 我們透過open_by_key這個method來開啟sheet
sheet = gss_client.open_by_key(spreadsheet_key_path)

# Get data from db
conn = sqlite3.connect('/home/pi/database/company_record.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM record')
row = 1
for result in cursor:
    x = "A"+str(row)
    sheet.sheet1.update(x, [result])
    row += 1
    print(result)
conn.close()
