import requests
from bs4 import BeautifulSoup
import json
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

class CreditLine:
    def __init__(self, balance_yest, selling_today, return_today, balance_today):
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
              sort_keys=True,
              indent=4
         )

def crawl_2317():
    url = 'https://www.twse.com.tw/rwd/zh/marginTrading/TWT93U?response=html'
    try:
        web = requests.get(url)
        soup = BeautifulSoup(web.text, "html5lib")
        stocks = soup.find_all('tr', attrs={"align":"center", "style":"font-size:14px;"})
        for stock in stocks:
            if stock.find('td').get_text() == "2317":
                stock_2317 = stock.find_all('td')

                balance_yest = stock_2317[8].get_text()  # 前日餘額
                selling_today = stock_2317[9].get_text() # 當日賣出
                return_today = stock_2317[10].get_text()  # 當日還券
                balance_today = stock_2317[12].get_text() # 今日餘額

                creditLine_2317 = CreditLine(balance_yest, selling_today, return_today, balance_today)
                return creditLine_2317.toJson()
    except:
        pass

def notify_discord_webhook():
    info = crawl_2317()
    url = "https://discord.com/api/webhooks/1356484738029719573/9GNCPHfl7gcz9BpkkO1xYEYqZ9_D2tWd0dx5sZqx3RTN3HgLFLql47TEgWYEsz0Q4x8g"   
    headers = {"Content-Type": "application/json"}
    data = {"content": info, "username": "newmanBot"}

    res = requests.post(url, headers = headers, json = data)
    
    if res.status_code in (200, 204):
            print(f"Request fulfilled with response code {res.status_code}")
    else:
            print(f"Request failed with response: {res.status_code}-{res.text}")\


def main(): 
    #  Non blocking Schedule
    scheduler.add_job(notify_discord_webhook, 'cron', day_of_week='1-5', hour=21, minute=00, second=00)
    scheduler.start()
    print('Schedule started ... - 21:00')
    
    cmdInput = None
    while cmdInput != "exit":
        print('Process is running ...')
        cmdInput = input("Command: ")

if __name__ == "__main__":
     main()