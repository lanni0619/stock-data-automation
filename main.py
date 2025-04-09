# Module
from datetime import datetime
from threading import Thread
import time
from logger import logger
from stock import Stock

def user_input_loop(stocks):
    while True:
        stock_code = int(input("📈 Enter 'stock code' or '0' to leave: "))

        if stock_code == 2317 or stock_code == 2330:
            while True:
                cmd = input("🔔 1)send_json 2)save_to_excel 3)send_chart 4)Get attribute 0)exit: ")
                if cmd == "1":
                    stocks[stock_code].send_json()
                elif cmd == "2":
                    stocks[stock_code].save_to_excel()
                elif cmd == "3":
                    stocks[stock_code].send_chart()
                elif cmd == "4":
                    print(stocks[stock_code].__dict__)
                elif cmd == '0':
                    break
                else:
                    print("Wrong cmd")
        elif stock_code == 0:
            print("Goodbye ...")
            break            

def main():
    logger.info("Start main ...")

    # 1) Preliminary
    stock2317 = Stock(2317)
    stock2330 = Stock(2330)
    
    stock2317.crawl_info()
    stock2330.crawl_info()
    
    stocks = {2317: stock2317, 2330: stock2330}

    # 2) Schedule work
    stock2317.schedule_task()
    stock2330.schedule_task()

    time.sleep(1)

    # 3) cli user interface
    user_input_loop(stocks)

if __name__ == "__main__":
    #  main()
    stock2317 = Stock(2317).crawl_info()
    stock2317.save_to_excel2()