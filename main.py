import time

from apscheduler.schedulers.background import BackgroundScheduler # type: ignore
import requests

# self-define
from config.config import config
from module.stock import Stock
import module.utils as utils
from module.logger import logger

scheduler:BackgroundScheduler = BackgroundScheduler(timezone="Asia/Taipei")

@utils.tic_tok
def stock_tasks(stocks_list:list["Stock"]) -> None:
    for stock in stocks_list:
        stock.fetch_price()
        stock.fetch_lending()
        stock.save_to_excel()
        stock.plot_grid_price_ss()

        if stock.stock_code == "2317":
            stock.json_to_dc_stock()
            stock.image_to_dc_stock()

        logger.info(f"[{stock.name_zh_tw}{stock.stock_code}] - Tasks are finished successfully")

def main() -> None:
    stocks_dict:dict = config.get("stock_code")
    stocks:list["Stock"] = [Stock(key, stocks_dict[key]) for key in stocks_dict]
    hour:int = 19
    minute:int = 52
    sec:int = 00
    day_of_week = "sat" # mon-fri

    scheduler.add_job(
        stock_tasks,
        'cron',
        day_of_week=day_of_week,
        hour=hour, minute=minute, second=sec,
        args=[stocks]
    )
    scheduler.start()

    while True:
        cmd = input("[CMD]:")
        if cmd == "0":
            print("Goodbye...")
            break

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {e}")
        logger.info("Restart after 30 seconds ...")
        time.sleep(30)
        main()
    except AttributeError as e:
        logger.error(f"Parsing error: {e}")
    except Exception as e:
        logger.error(f"Exception: {e}")