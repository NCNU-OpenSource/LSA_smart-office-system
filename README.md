# LSA_smart-office-system

## Telegram Bot
* Bot name: Office Genie
* Bot id: @officetooladmin_bot
* ![](https://i.imgur.com/NulvJMF.png)
## 動機

## 使用設備


![](https://i.imgur.com/eWJEnu0.png)

![](https://i.imgur.com/RUixRIZ.jpg)


1. RFID RC522
![](https://i.imgur.com/OyUmgGY.png)


| RC522 接口 | Raspberry Pi 接口 | 
| -------- |  -------- |
| 3.3v     | Pin17     | 
| RST      | Pin22     | 
| GDN      | Pin20     | 
| MISO     | Pin21     | 
| MOSI     | Pin19     | 
| SCK      | Pin23     | 
| SAD      | Pin24     | 


2. L9110 風扇模組
![](https://i.imgur.com/i2cEcnK.png)

| 風扇模組 接口 | Raspberry Pi 接口 | 
| -------- | -------- | 
| VCC (5v)       | 麵包板 +      | 
| Ground (-) | 麵包板 -     | 
| INA | Pin 16     | 
| INB | Pin 18     | 


3. 雨水檢測
- MH-RD
    - ![](https://i.imgur.com/9czppqf.png)
    - 
| KY-016 接口 | Raspberry Pi 接口 | 
| -------- | -------- | 
| VCC (3.3v)       | Pin 1      | 
| Ground (-) | 麵包板 -     | 
| DO (data) | Pin 8     | 


4. 温度控制
- 室內DHT11 溫度/濕度感應器
    - ![](https://i.imgur.com/QDvWYLq.jpg)

| 室內DHT11 接口 | Raspberry Pi 接口 | 
| -------- | -------- | 
| 5v (VCC)       | 麵包板 +      | 
| Ground (GDN) | 麵包板 -     | 
| Signal (data)| Pin 12    | 

| 室外DHT11 接口 | Raspberry Pi 接口 | 
| -------- | -------- | 
| 5v (VCC)       | 麵包板 +      | 
| Ground (GDN) | 麵包板 -     | 
| Signal (data)| Pin 10    | 

- KY-016 RGB LED 模組
    - ![](https://i.imgur.com/xuxnFlO.png)

| KY-016 接口 | Raspberry Pi 接口 | 
| -------- | -------- | 
| R       | Pin 11      | 
| Ground (-) | 麵包板 -     | 

![](https://i.imgur.com/BSKcvj2.png)

| 零件名稱|價格|應用| 
| -------- | -------- |  -------- |
| RC522 | NT$39 | 門禁打卡系統 |
| SG90 | NT$30 | 門閘展示 |
| DHT11 | NT$45 | 溫度感測 |
| MH-RD | NT$50 | 雨滴感測 |
| L9110 | NT$150 | 訊號展示 |

* breadboard layout:

![](https://i.imgur.com/QztGPV8.jpg)

## 使用技術

## 功能
1. 辨公室同事可透過telegram bot中得知室外溫度
2. 辨公室同事可透過telegram bot中得知公司附近有否下雨
3. 辨公室冷氣主管可透過telegram bot控制冷氣開關
4. 辨公室同事能透過上下班刷卡開啟公司大門進出
5. 辨公室人事部同事能查看同事上下班刷卡紀錄

## RFID門禁系統實作
### 開啟Raspberry Pi 的SPI
- 進入 Raspberry Pi Config
    - `sudo raspi-config`
- Interfacing Options
    - ![](https://i.imgur.com/YBef2VM.png)
- SPI
    - ![](https://i.imgur.com/bQ46ayo.png)
- Enabled > Yes
    - ![](https://i.imgur.com/B6WR94c.png)
- 重新開機
    - `sudo reboot`
- 查是否正常啟動
    - `lsmod | grep spi`
    - 出現spi_bcm2835為成功 
    - ![](https://i.imgur.com/r11emNa.png)

### 安裝Python
- 首先更新套件
    - `sudo apt-get update`
    - `sudo apt-get upgrade`
- 安裝Python及相關套件 
    - `sudo apt-get install python3-dev python3-pip`
    - `sudo pip3 install spidev`
    - `sudo pip3 install mfrc522`
    - `sudo pip3 install datetime`
    - 如果出現 ModuleNotFoundError: No module named 'mfrc522', 可以嘗試把套件更新

        - `sudo pip install mfrc522 --upgrade`
        - `sudo pip install mfrc522 --updatev`

### 讀取RFID卡片測試
- 新增RFID文件夾及Python文件
    - `mkdir ~/pi-rfid`
    - `cd ~/pi-rfid`
    - `sudo vim read.py`
- Python文件內輸入
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
- 運行Python檔案
    - `sudo python3 read.py`
- 拍卡
    - ![](https://i.imgur.com/jyjEAPd.jpg)
- 讀取成功會出現卡片ID
    - ![](https://i.imgur.com/77mRPMf.png)

### 連接 Servo Motor 到 Raspberry Pi
![](https://i.imgur.com/miBkv5L.jpg)

| Servo Motor 接口 | Raspberry Pi 接口 | 
| -------- | -------- |
| 5v (Red)       | Pin2     | 
| Ground (Brown) | Pin9     | 
| Signal (Orange)| Pin7     | 

### Servo Motor測試
- 新增Python文件
    - `sudo vim test_servomotor.py`
- Python文件內輸入

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
- 運行Python檔案
    - `sudo python3 test_servomotor.py`
    - ![](https://i.imgur.com/1Sad5a6.gif)

### 上下班打卡及門禁系統 

- 安裝SQLite及新增資料庫文件夾 
    - `sudo apt-get install sqlite3`
    - `sudo mkdir -m 777 ~/database`

- 新增員工
    - 運行 new_staff.py
        - `sudo python3 new_staff.py`
    - Input your name: (輸入員工姓名後按Enter)
    - Now place your tag to write (用空白的RFID卡拍卡)
    - 完成後會出現 Data added successfully
    - ![](https://i.imgur.com/DDJ1VwT.png)

- 門禁系統
    - 運行 access_control.py
    - `sudo python3 access_control.py`
    - Now place your tag to read (用已新增員工的RFID卡拍卡)
    - 成功後會出現 Login successfully 及 閘門將會打開
        - ![](https://i.imgur.com/LWWpTLt.png)
        - ![](https://i.imgur.com/amDNzNA.gif)

    - 如非本公司資料庫內的員工, 將會出現 Login failed 及 閘門不會開啟
        - ![](https://i.imgur.com/AArB4wC.png)
        - ![](https://i.imgur.com/NPEsThQ.gif)

- 上下班打卡紀錄
    - 假如上面步驟出現Login successfully後, database資料夾內會自動生成一個 company_record.db 檔案
    - 將檔案匯出後使用[DB Browser for SQLite](https://sqlitebrowser.org/)瀏覽company_record.db檔案, 可發現已新增員工上下班紀錄
    - ![](https://i.imgur.com/gKfkUVK.png)


## 匯出資料庫至CSV
- 運行`exportcsv.py`, csv檔案將會匯出至database資料夾裡面
- `python3 exportcsv.py`



## 打卡紀錄同步至Google Sheet
### Google Sheet API申請憑證
- 1. 先建立專案
![](https://i.imgur.com/WH4NpNY.png)
- 點選左上方選取專案
![](https://i.imgur.com/quT1GeJ.png)
- 建立一個專案
![](https://i.imgur.com/fHpnzcv.png)
- 確認切換專案成功
![](https://i.imgur.com/WWsuase.png)
- 2. 啟用 Google Sheet API, 點選 ENABLE APPS AND SERVICES
![](https://i.imgur.com/XoUn7oE.png)
- 找一下 google sheet
![](https://i.imgur.com/IqwnfwD.png)
- 啟用
![](https://i.imgur.com/TnSGjl6.png)
- 3. 新增憑證, 切換到憑證的頁面點選建立憑證的服務帳戶
![](https://i.imgur.com/KzblyuY.png)
- 沒有特殊需求就可以直接按繼續
![](https://i.imgur.com/QmrYUBR.png)
- 這邊也是，沒有特殊需求就可以直接按繼續
![](https://i.imgur.com/IGq9Nav.png)
- 建立完成後應該會有多一個服務帳戶點擊那個服務帳戶
![](https://i.imgur.com/Td7Bncq.png)
- 新增金鑰
![](https://i.imgur.com/rYcdn7y.png)
- 選擇 JSON
![](https://i.imgur.com/HWVm0Is.png)
- 他會自動幫你下載下來, 請把他重新命名為auth.json並放到googlesheet_update.py同一目錄下
![](https://i.imgur.com/Wpb2q6S.png)

### Google Sheet API開啟權限
- 1. 點選共用
![](https://i.imgur.com/FrItZhu.png)
- 2. 輸入你剛剛申請的服務帳號信箱地址
![](https://i.imgur.com/vmloQsj.png)


### API 串接
- 先在pi安裝套件
- `pip install gspread`
- `pip install oauth2client`
- 查找google sheet 網址, 將google sheet 網址紅色地方複製
![](https://i.imgur.com/BDhE4pn.png)
- 到`googlesheet_update.py`進行修改, 在第17行spreadsheet_key_path填入剛剛複製的紅色地方字串
![](https://i.imgur.com/cJDREbz.png)
- 最後直接運行`googlesheet_update.py`就可自動同步database到google sheet
- `python3 googlesheet_update.py`

## 建立Telegram Bot
1. 先在手機應用程式商店下載Telegram Messenger

![](https://i.imgur.com/7bTwXUU.jpg)

2. 下載完成後申請帳號，再利用搜尋欄搜尋"BotFather"，並點擊BotFather (注意:有藍勾的才是官方認證機器人!)

![](https://i.imgur.com/tR8WB7K.jpg)

3. 在對話中輸入"/start"

![](https://i.imgur.com/epNi844.jpg)

4. 接著輸入"/newbot"建立新機器人

![](https://i.imgur.com/rZpbY0Q.jpg)

5. 輸入"Your_Bot_Name"為機器人建立名稱

![](https://i.imgur.com/o4qyzY0.jpg)

6. 輸入"Your_Bot_ID"為機器人建立user id (user id為獨一無二，其他user能夠在搜尋欄輸入機器人user id並使用它)

![](https://i.imgur.com/9e6IaN3.jpg)

7. 完成以上步驟後，BotFather會在訊息中給予一組token，我們需要把token放在所需要的程式中並運行起來，這樣Telegram Bot的基本設定就完成囉!

![](https://i.imgur.com/qLFsMHI.jpg)
