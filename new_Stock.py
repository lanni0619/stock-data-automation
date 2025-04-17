# standard
from datetime import datetime
from typing import Optional

# Self-define module
import utils
from crawler import Crawler
from dc_stock_channel import DcStockChannel
from logger import logger

class Stock:
    def __init__(self, stock_code: int):
        self.stock_code:int = stock_code
        self.price:Optional[str] = None
        self.balance_yest:Optional[str] = None
        self.selling_today:Optional[str] = None
        self.return_today:Optional[str] = None
        self.balance_today:Optional[str] = None
        self.updatetime:Optional[str] = None
    
    def fetch_price(self) -> None:
        self.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.price = Crawler.crawl_price(self.stock_code)
    
    def fetch_lending(self) -> None:
        results:list[str] = Crawler.crawl_lending(self.stock_code)
        self.balance_yest = results[0]
        self.selling_today = results[1]
        self.return_today = results[2]
        self.balance_today = results[3]
        self.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def json2webhook(self) -> None:
        if(utils.all_attrs_not_none(self)):
            DcStockChannel.send_json(utils.json_stringify(self))
            return
        
        logger.error(f"[{__name__}.json2webhook] - attrs have None")


if __name__ == "__main__":
    stock2317 = Stock(2317)
    stock2317.fetch_price()
    stock2317.fetch_lending()
    stock2317.json2webhook()