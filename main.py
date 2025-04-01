import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd

import json
from datetime import datetime
import os
import sys
import time

scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

class CreditLine:
    def __init__(self, date, balance_yest, selling_today, return_today, balance_today):
        self.date = date
        self.balance_yest = balance_yest
        self.selling_today = selling_today
        self.return_today = return_today
        self.balance_today = balance_today
        self.unit = "share"
    def toJson(self):
        #  https://stackoverflow.com/questions/7408647/convert-dynamic-python-object-to-json
         return json.dumps(
              self,
              default=lambda o: o.__dict__,
              sort_keys=False,
              indent=4
         )

def crawl_2317():
    url = 'https://www.twse.com.tw/rwd/zh/marginTrading/TWT93U?response=html'
    web = requests.get(url)
    soup = BeautifulSoup(web.text, "html5lib")
    stocks = soup.find_all('tr', attrs={"align":"center", "style":"font-size:14px;"})
    for stock in stocks:
        if stock.find('td').get_text() == "2317":
            stock_2317 = stock.find_all('td')

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            balance_yest = stock_2317[8].get_text()  # 前日餘額
            selling_today = stock_2317[9].get_text() # 當日賣出
            return_today = stock_2317[10].get_text()  # 當日還券
            balance_today = stock_2317[12].get_text() # 今日餘額

            creditLine_2317 = CreditLine(date, balance_yest, selling_today, return_today, balance_today)
            return creditLine_2317

def notify_discord_webhook():
    # Preliminary
    info = crawl_2317()
    info_json = info.toJson()
    url = "https://discord.com/api/webhooks/1356484738029719573/9GNCPHfl7gcz9BpkkO1xYEYqZ9_D2tWd0dx5sZqx3RTN3HgLFLql47TEgWYEsz0Q4x8g"   
    headers = {"Content-Type": "application/json"}
    data = {"content": info_json, "username": "newmanBot"}

    # Write to log
    save_to_excel(info, 2317)

    # Send data to discord
    res = requests.post(url, headers = headers, json = data)
    
    # Read the response
    if res.status_code in (200, 204):
            print(f"Request fulfilled with response code {res.status_code}")
    else:
            print(f"Request failed with response: {res.status_code}-{res.text}")

def save_to_logFile(info, stock_number):
    root_path = "C:/temp/stock-log"

    file_path = os.path.join(root_path, f"{stock_number}-file.txt")
    with open(file_path, 'a') as file:
         file.write('Date: ' + info.date + '\n')
         file.write('balance_yest: ' + info.balance_yest + '\n')
         file.write('selling_today: ' + info.selling_today + '\n')
         file.write('return_today: ' + info.return_today + '\n')
         file.write('balance_today: ' + info.balance_today + '\n')

def save_to_excel(info, stock_number):
    today = datetime.today()
    root_path = "C:/temp/stock-log"
    filename = os.path.join(root_path, f"{stock_number}_{today.strftime('%Y-%m')}.xlsx")
    new_entry = {
    "date": info.date,
    "balance_yest": int(info.balance_yest.replace(",", "")),
    "balance_today": int(info.balance_today.replace(",", "")),
    "return_today": int(info.return_today.replace(",", "")),
    "balance_today": int(info.balance_today.replace(",", "")),
    }

    # 檢查檔案是否存在
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])

    df.to_excel(filename, index=False)
    print(f"✅ {info.date} 紀錄已存入 {filename}")

def main(): 
    #  Non blocking Schedule
    scheduler.add_job(notify_discord_webhook, 'cron', day_of_week='1-5', hour=21, minute=00, second=00)
    scheduler.start()
    print('Schedule at 21:00 every Monday to Friday ...')
    
    # Let process non-stop
    cmdInput = None
    while cmdInput != "0":
        print('Process is running ...')
        cmdInput = input("Command: ")
        if cmdInput == str(1):
            notify_discord_webhook()

if __name__ == "__main__":
     main()