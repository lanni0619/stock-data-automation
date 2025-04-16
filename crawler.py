# 3rd party package
import requests
from requests import Response
from bs4 import BeautifulSoup, Tag, NavigableString, ResultSet
# apscheduler don't have official stub
from apscheduler.schedulers.background import BackgroundScheduler # type: ignore

# Standard module
from datetime import datetime
from typing import Any, Callable, Optional, Union, cast

# Custom module
from logger import logger
from decorator import tic_tok

class crawler:
    stockprice_url = "https://tw.stock.yahoo.com/quote/{0}.TW"
    twse_margintrading_url = "https://www.twse.com.tw/rwd/zh/marginTrading/TWT93U?response=html"
    price_classes: list[str] = [
        "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",  # 漲
        "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",  # 跌
        "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",  # 平盤
        "Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-down)",  # 跌停
        "Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-up)",  # 漲停
    ]

    @classmethod
    @tic_tok
    def crawl_price(self, stock_code:int) -> Optional[list]:
        try:
            logger.info(f"[crawler.crawl_price] - stock_number = {stock_code}")
            url:str = self.stockprice_url.format(stock_code)
            web:Response = requests.get(url)
            soup:BeautifulSoup = BeautifulSoup(web.text, "html5lib")

            span_tag:Union[Tag, NavigableString, None] = soup.find('span', class_=lambda x: x and any(cls in x for cls in self.price_classes))
            if isinstance(span_tag, Tag):
                price: str = span_tag.get_text()
                logger.info(f"[crawler.crawl_price] - Get price = {price}")
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return [price, created_at]
            else:
                raise Exception(f"[crawler.crawl_price] - Fail to get {stock_code} price")

        except requests.exceptions.RequestException as e:
            logger.error(f"[crawler.crawl_price] - Network error: {e}")
        except AttributeError as e:
            logger.error(f"[crawler.crawl_price] - Parsing error: {e}")
        except Exception as e:
            logger.error(f"[crawler.crawl_price] - unexpected error: {e}")
        return None

    @classmethod
    @tic_tok
    def crawl_short_selling(self, stock_code:int) -> object:
        try:
            logger.info(f"[crawler.crawl_short_selling] - stock_number = {stock_code}")
            url:str = self.twse_margintrading_url
            web:Response = requests.get(url)
            soup:BeautifulSoup = BeautifulSoup(web.text, "html5lib")
            trs:ResultSet = soup.find_all('tr', attrs={"align":"center", "style":"font-size:14px;"})

            for tr in trs:
                if tr.find('td').get_text() == str(stock_code):
                    target_info = tr.find_all('td')
                    self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._balance_yest = target_info[8].get_text()  # 前日餘額
                    self._selling_today = target_info[9].get_text() # 當日賣出
                    self._return_today = target_info[10].get_text()  # 當日還券
                    self._balance_today = target_info[12].get_text() # 今日餘額 
                    logger.info(f"[crawler.crawl_short_selling] - Get info = {self.__dict__}")
                    return self

            raise Exception(f"[crawler.crawl_short_selling] - Could not find {stock_code} short_selling info")

        except requests.exceptions.RequestException as e:
            logger.error(f"[crawler.crawl_short_selling] - Network error: {e}")
        except AttributeError as e:
            logger.error(f"[crawler.crawl_short_selling] - Parsing error: {e}")
        except Exception as e:
            logger.error(f"[crawler.crawl_short_selling] - unexpected error: {e}")
        return None
    
if __name__ == "__main__":
    print(crawler.crawl_price(2317))