# Package
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd

# Module
import json
from datetime import datetime
import os
import threading
import sys
import time
from module.matplotlib_demo import plot_short_selling

# Global variable
info_2317 = None

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
    global info_2317
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

            info_2317 = CreditLine(date, balance_yest, selling_today, return_today, balance_today)

def send_json_discord(info):
    # Preliminary
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
            print(f"✅ Request fulfilled with response code {res.status_code}")
    else:
            print(f"❌ Request failed with response: {res.status_code}-{res.text}")
    print("")

def send_jpg_discord(stock_number):
    # draw new chart
    plot_short_selling(stock_number)

    # Path to the JPG file
    today = datetime.today()
    jpg_file_path = f"C:/temp/stock-log/{stock_number}_{today.strftime('%Y-%m')}.jpg"  # Replace with your actual file name

    # Discord webhook URL
    url = "https://discord.com/api/webhooks/1356484738029719573/9GNCPHfl7gcz9BpkkO1xYEYqZ9_D2tWd0dx5sZqx3RTN3HgLFLql47TEgWYEsz0Q4x8g"

    # Check if the file exists
    if not os.path.exists(jpg_file_path):
        print(f"❌ File not found: {jpg_file_path}")
        return

    # Prepare the file and payload
    with open(jpg_file_path, "rb") as file:
        files = {"file": (os.path.basename(jpg_file_path), file, "image/jpeg")}
        payload = {"username": "newmanBot"}

        # Send the request
        res = requests.post(url, data=payload, files=files)

    # Read the response
    if res.status_code in (200, 204):
        print(f"✅ JPG file sent successfully with response code {res.status_code}")
    else:
        print(f"❌ Failed to send JPG file: {res.status_code} - {res.text}")
    print("")

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
        "selling_today": int(info.selling_today.replace(",", "")),
        "return_today": int(info.return_today.replace(",", "")),
        "balance_today": int(info.balance_today.replace(",", ""))
    }
    print(filename)
    # 檢查檔案是否存在
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])

    df.to_excel(filename, index=False)
    print(f"✅ {info.date} 紀錄已存入 {filename}")
    print("")

def build_allData_2317():
    # Preliminary
    global info_2317
    hour = 21
    min = 00
    
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    
    # Non blocking Schedule
    scheduler.add_job(crawl_2317, 'cron', day_of_week='1-5', hour=hour, minute=00, second=00)
    scheduler.add_job(lambda: send_json_discord(info_2317), 'cron', day_of_week='1-5', hour=hour, minute=min, second=15)
    print(f"Schedule send_json_discord at {hour}:00:00 on Monday to Friday ...")
    
    scheduler.add_job(lambda: send_jpg_discord(2317), 'cron', day_of_week='5', hour=hour, minute=min, second=30)
    print(f"Schedule send_jpg_discord at {hour}:00:30 on Friday !")

    scheduler.start()

def user_input_loop():
    while True:
        print('👍 Process is running ...')
        cmd = input("🔔 Command: ")
        
        if cmd == "0":
            print("Exiting...")
            break
        
        elif cmd == "1":
            crawl_2317()
            send_json_discord(info_2317)
        
        elif cmd == "2":
            send_jpg_discord(2317)

        elif cmd == "3":
            print("info_2317 = ", info_2317)


def main(): 
    scheduler_thread = threading.Thread(target=build_allData_2317)
    scheduler_thread.start()

    time.sleep(1)
    user_input_loop()

if __name__ == "__main__":
     main()