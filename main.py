# Module
import time

from module.logger import logger
from module.stock import Stock

def user_input_loop(stocks:dict) -> None:
    while True:
        stock_code:int = int(input("📈 Enter 'stock code' or '0' to exit: "))

        if stock_code == 2317 or stock_code == 2330:
            while True:
                cmd:str = input("🔔 (1)send_json (2)save_to_excel (3)send_chart (4)Get price (5)Get short selling (0)return: ")
                if cmd == "1":
                    stocks[stock_code].send_json()
                elif cmd == "2":
                    stocks[stock_code].save_to_excel()
                elif cmd == "3":
                    stocks[stock_code].send_chart()
                elif cmd == "4":
                    stocks[stock_code].crawl_price()
                elif cmd == "5":
                    stocks[stock_code].crawl_short_selling()
                elif cmd == '0':
                    break
                else:
                    print("Wrong cmd")
        elif stock_code == 0:
            print("Goodbye ...")
            break            

def main() -> None:
    logger.info("Start main ...")

    try:
         # 1) Preliminary
        stock2317:Stock = Stock(2317)
        stock2330:Stock = Stock(2330)
        
        stocks:dict = {2317: stock2317, 2330: stock2330}

        # 2) Schedule work
        stock2317.schedule_task()
        stock2330.schedule_task()

        # 3) cli user interface
        user_input_loop(stocks)
    
    except Exception as e:
        logger.error(e)
        logger.error("Something went wrong, restart after 1 min ...")
        time.sleep(60)
        main()


if __name__ == "__main__":
     main()