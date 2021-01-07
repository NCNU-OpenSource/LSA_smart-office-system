# LSA_smart-office-system

## Telegram Bot

- Bot name: Office Genie
- Bot id: @officetooladmin_bot
- ![](https://i.imgur.com/NulvJMF.png)

## 動機

- 組內成員們在企業實習的過程中，遇到的一些小困擾問題，產生的一個小小 Bot 系統去讓這些懶惰的人更快樂地懶惰下去。
- 困擾(故事)
  - A 同學在人事部實習，每個月都要將辦公室內所有人的出勤卡上下班時間，一張一張的打進 excel 裡面然後再製作薪資表單。
  - B 同學在機房實習，機房內外都沒有窗戶，樓層又高，中午吃飯的時候常要搭好久的電梯下去，如果遇上外頭下雨又要搭好久的電梯上樓。
  - C 同學家離公司有一大段距離，常常騎到公司附近之後才覺得很冷應該多穿一件衣服，但有時運氣不好，多穿一件衣服時又覺得熱。
  - A、C 同學的辦公室內冷氣開放都是由主管管控，但很常因為主管不在位置上沒人去開冷氣覺得很熱，希望室內溫度超過設定溫度時自動開啟冷氣。
  - D 同學聽著同學們的種種抱怨，熱心的他決定來幫大家解決這些小困擾！

## 功能

1. 辨公室同事可透過 telegram bot 中得知室外溫度
2. 辨公室同事可透過 telegram bot 中得知公司附近有否下雨
3. 辨公室冷氣主管可透過 telegram bot 控制冷氣開關
4. 辨公室同事能透過上下班刷卡開啟公司大門進出
5. 辨公室人事部同事能查看同事上下班刷卡紀錄

## 使用設備

1. Raspberry pi 3

   <img src="https://i.imgur.com/eWJEnu0.png" width="375">

   <img src="https://i.imgur.com/RUixRIZ.jpg" width="375">

1. RFID RC522

   <img src="https://i.imgur.com/OyUmgGY.png" width="375">

| RC522 接口 | Raspberry Pi 接口 |
| ---------- | ----------------- |
| 3.3v       | Pin17             |
| RST        | Pin22             |
| GDN        | Pin20             |
| MISO       | Pin21             |
| MOSI       | Pin19             |
| SCK        | Pin23             |
| SAD        | Pin24             |

2. L9110 風扇模組

<img src="https://i.imgur.com/i2cEcnK.png" width="375">

| 風扇模組 接口 | Raspberry Pi 接口 |
| ------------- | ----------------- |
| VCC (5v)      | 麵包板 +          |
| Ground (-)    | 麵包板 -          |
| INA           | Pin 16            |
| INB           | Pin 18            |

3. 雨水檢測

- MH-RD -
  <img src="https://i.imgur.com/9czppqf.png" width="375">
  | KY-016 接口 | Raspberry Pi 接口 |
  | -------- | -------- |
  | VCC (3.3v) | Pin 1 |
  | Ground (-) | 麵包板 - |
  | DO (data) | Pin 8 |

4. 溫度控制

- 室內 DHT11 溫度/濕度感應器  
  <img src="https://i.imgur.com/QDvWYLq.jpg" width="375">

| 室內 DHT11 接口 | Raspberry Pi 接口 |
| --------------- | ----------------- |
| 5v (VCC)        | 麵包板 +          |
| Ground (GDN)    | 麵包板 -          |
| Signal (data)   | Pin 12            |

| 室外 DHT11 接口 | Raspberry Pi 接口 |
| --------------- | ----------------- |
| 5v (VCC)        | 麵包板 +          |
| Ground (GDN)    | 麵包板 -          |
| Signal (data)   | Pin 10            |

<img src="https://i.imgur.com/BSKcvj2.png" width="375">

| 零件名稱 | 價格   | 應用         |
| -------- | ------ | ------------ |
| RC522    | NT$39  | 門禁打卡系統 |
| SG90     | NT$30  | 門閘展示     |
| DHT11    | NT$45  | 溫度感測     |
| MH-RD    | NT$50  | 雨滴感測     |
| L9110    | NT$150 | 訊號展示     |

- breadboard layout:
  <img src="https://i.imgur.com/QztGPV8.jpg" width="375">

## 使用技術

## RFID 門禁系統實作

### 開啟 Raspberry Pi 的 SPI

- 進入 Raspberry Pi Config
  - `sudo raspi-config`
- Interfacing Options
  - <img src="https://i.imgur.com/YBef2VM.png" width="375">
- SPI
  - <img src="https://i.imgur.com/bQ46ayo.png" width="375">
- Enabled > Yes
  - <img src="https://i.imgur.com/B6WR94c.png" width="375">
- 重新開機
  - `sudo reboot`
- 查是否正常啟動
  - `lsmod | grep spi`
  - 出現 spi_bcm2835 為成功
  - <img src="https://i.imgur.com/r11emNa.png" width="375">

### 安裝 Python

- 首先更新套件
  - `sudo apt-get update`
  - `sudo apt-get upgrade`
- 安裝 Python 及相關套件

  - `sudo apt-get install python3-dev python3-pip`
  - `sudo pip3 install spidev`
  - `sudo pip3 install mfrc522`
  - `sudo pip3 install datetime`
  - 如果出現 ModuleNotFoundError: No module named 'mfrc522', 可以嘗試把套件更新

    - `sudo pip install mfrc522 --upgrade`
    - `sudo pip install mfrc522 --updatev`

### 讀取 RFID 卡片測試

- 新增 RFID 文件夾及 Python 文件
  - `mkdir ~/pi-rfid`
  - `cd ~/pi-rfid`
  - `sudo vim read.py`
- Python 文件內輸入

```python
#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        id, text = reader.read()
        print(id)
        #print(text)
finally:
        GPIO.cleanup()

```

- 運行 Python 檔案
  - `sudo python3 read.py`
- 拍卡
  - <img src="https://i.imgur.com/jyjEAPd.jpg" width="375">
- 讀取成功會出現卡片 ID
  - <img src="https://i.imgur.com/77mRPMf.png" width="375">

### 連接 Servo Motor 到 Raspberry Pi

<img src="https://i.imgur.com/miBkv5L.jpg" width="375">

| Servo Motor 接口 | Raspberry Pi 接口 |
| ---------------- | ----------------- |
| 5v (Red)         | Pin2              |
| Ground (Brown)   | Pin9              |
| Signal (Orange)  | Pin7              |

### Servo Motor 測試

- 新增 Python 文件
  - `sudo vim test_servomotor.py`
- Python 文件內輸入

```python
# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 7 as an output, and set servo1 as pin 7 as PWM
GPIO.setup(7, GPIO.OUT)
servo1 = GPIO.PWM(7, 50)  # Note 7 is pin, 50 = 50Hz pulse


def dooropen(servo1):
    # start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    print("Motor start")

    # Turn back to 90 degrees
    print("Turning to 90 degrees")
    servo1.ChangeDutyCycle(7)
    time.sleep(1)

    # turn back to 0 degrees
    print("Turning back to 0 degrees")
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

    # Clean things up at the end
    servo1.stop()
    GPIO.cleanup()


dooropen(servo1)
```

- 運行 Python 檔案
  - `sudo python3 test_servomotor.py`
  - <img src="https://i.imgur.com/1Sad5a6.gif" width="375">

### 上下班打卡及門禁系統

- 安裝 SQLite 及新增資料庫文件夾

  - `sudo apt-get install sqlite3`
  - `sudo mkdir -m 777 ~/database`

- 新增員工

  - 運行 new_staff.py
    - `sudo python3 new_staff.py`
  - Input your name: (輸入員工姓名後按 Enter)
  - Now place your tag to write (用空白的 RFID 卡拍卡)
  - 完成後會出現 Data added successfully
  - <img src="https://i.imgur.com/DDJ1VwT.png" width="375">

- 門禁系統

  - 運行 access_control.py
  - `sudo python3 access_control.py`
  - Now place your tag to read (用已新增員工的 RFID 卡拍卡)
  - 成功後會出現 Login successfully 及 閘門將會打開

    - <img src="https://i.imgur.com/LWWpTLt.png" width="375">
    - <img src="https://i.imgur.com/amDNzNA.gif" width="375">

  - 如非本公司資料庫內的員工, 將會出現 Login failed 及 閘門不會開啟
    - <img src="https://i.imgur.com/AArB4wC.png" width="375">
    - <img src="https://i.imgur.com/NPEsThQ.gif" width="375">

- 上下班打卡紀錄
  - 假如上面步驟出現 Login successfully 後, database 資料夾內會自動生成一個 company_record.db 檔案
  - 將檔案匯出後使用[DB Browser for SQLite](https://sqlitebrowser.org/)瀏覽 company_record.db 檔案, 可發現已新增員工上下班紀錄
  - <img src="https://i.imgur.com/gKfkUVK.png" >

## 匯出資料庫至 CSV

- 運行`exportcsv.py`, csv 檔案將會匯出至 database 資料夾裡面
- `python3 exportcsv.py`

## 打卡紀錄同步至 Google Sheet

### Google Sheet API 申請憑證

- 1. 先建立專案
     - <img src="https://i.imgur.com/WH4NpNY.png" width="375">
- 點選左上方選取專案
  - <img src="https://i.imgur.com/quT1GeJ.png" width="375">
- 建立一個專案
  - <img src="https://i.imgur.com/fHpnzcv.png" width="375">
- 確認切換專案成功
  - <img src="https://i.imgur.com/WWsuase.png" width="375">
- 2. 啟用 Google Sheet API, 點選 ENABLE APPS AND SERVICES
     - <img src="https://i.imgur.com/XoUn7oE.png" width="375">
- 找一下 google sheet
  - <img src="https://i.imgur.com/IqwnfwD.png" width="375">
- 啟用
  - <img src="https://i.imgur.com/TnSGjl6.png" width="375">
- 3. 新增憑證, 切換到憑證的頁面點選建立憑證的服務帳戶
     - <img src="https://i.imgur.com/KzblyuY.png" width="375">
- 沒有特殊需求就可以直接按繼續
  - <img src="https://i.imgur.com/QmrYUBR.png" width="375">
- 這邊也是，沒有特殊需求就可以直接按繼續
  - <img src="https://i.imgur.com/IGq9Nav.png" width="375">
- 建立完成後應該會有多一個服務帳戶點擊那個服務帳戶
  - <img src="https://i.imgur.com/Td7Bncq.png" width="375">
- 新增金鑰
  - <img src="https://i.imgur.com/rYcdn7y.png" width="375">
- 選擇 JSON
  - <img src="https://i.imgur.com/HWVm0Is.png" width="375">
- 他會自動幫你下載下來, 請把他重新命名為 auth.json 並放到 googlesheet_update.py 同一目錄下
  - <img src="https://i.imgur.com/Wpb2q6S.png" width="375">

### Google Sheet API 開啟權限

- 1. 點選共用
     - <img src="https://i.imgur.com/FrItZhu.png" width="375">
- 2. 輸入你剛剛申請的服務帳號信箱地址
     - <img src="https://i.imgur.com/K0cGABK.png" width="375">

### API 串接

- 先在 pi 安裝套件
- `pip install gspread`
- `pip install oauth2client`
- 查找 google sheet 網址, 將 google sheet 網址橘色地方複製
  - <img src="https://i.imgur.com/gKfkUVK.png" width="375">![](https://i.imgur.com/BDhE4pn.png)
- 到`googlesheet_update.py`進行修改, 在第 17 行 spreadsheet_key_path 填入剛剛複製的紅色地方字串
  - <img src="https://i.imgur.com/gKfkUVK.png" width="375">![](https://i.imgur.com/cJDREbz.png)
- 最後直接運行`googlesheet_update.py`就可自動同步 database 到 google sheet
- `python3 googlesheet_update.py`

## 建立 Telegram Bot

1. 先在手機應用程式商店下載 Telegram Messenger

   - <img src="https://i.imgur.com/7bTwXUU.jpg" width="375">

2. 下載完成後申請帳號，再利用搜尋欄搜尋"BotFather"，並點擊 BotFather (注意:有藍勾的才是官方認證機器人!)

   - <img src="https://i.imgur.com/tR8WB7K.jpg" width="375">

3. 在對話中輸入"/start"

   - <img src="https://i.imgur.com/epNi844.jpg" width="375">

4. 接著輸入"/newbot"建立新機器人

   - <img src="https://i.imgur.com/rZpbY0Q.jpg" width="375">

5. 輸入"Your_Bot_Name"為機器人建立名稱

   - <img src="https://i.imgur.com/o4qyzY0.jpg" width="375">

6. 輸入"Your_Bot_ID"為機器人建立 user id (user id 為獨一無二，其他 user 能夠在搜尋欄輸入機器人 user id 並使用它)

   - <img src="https://i.imgur.com/9e6IaN3.jpg" width="375">

7. 完成以上步驟後，BotFather 會在訊息中給予一組 token，我們需要把 token 放在所需要的程式中並運行起來，這樣 Telegram Bot 的基本設定就完成囉!

   - <img src="https://i.imgur.com/qLFsMHI.jpg" width="375">

## 在自身 ubuntu 主機設定 Mosquitto

1. 安裝 Mosquitto `sudo apt-get install mosquitto`

2. 檢查是否順利安裝 `cd etc/mosquitto` (看看這個資料夾底下有沒有設定檔)

3. 在 conf 檔案中新增 2 行 Code `sudo vim mosquitto.conf ` (分別為放帳密的檔案的位置以及是否開啟匿名操作)
- `password_file /etc/mosquitto/passwd` 
放帳號與密碼的檔案，需要自己創建在/etc/mosquitto底下
- `allow anonymous true/false `
為了方便以下操作我們將它設成 true，如果將匿名設為false的話，不管是訂閱者或是推送者皆要輸入帳密才能向broker訂閱資料或推送資料，帳密儲存在broker的帳密檔內，也就是上面提到的路徑 
- 
