# LSA_smart-office-system

## Telegram Bot
* Bot name: Office Genie
* Bot id: @officetooladmin_bot
* ![](https://i.imgur.com/NulvJMF.png)
## 動機

## 使用設備

1. RFID RC522

![](https://i.imgur.com/eWJEnu0.png)

![](https://i.imgur.com/RUixRIZ.jpg)

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
