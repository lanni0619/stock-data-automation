# 3rd party package
import requests
from requests import Response
from bs4 import BeautifulSoup, Tag, NavigableString, ResultSet

# Standard module
from typing import Union, cast, Optional

# Custom module
from module.logger import logger
import module.utils as utils

class CrawlerConfig:
    BASE_URL = "https://tw.stock.yahoo.com/quote/{0}.TW"
    LENDING_URL = "https://www.twse.com.tw/rwd/zh/marginTrading/TWT93U?response=html"
    PRICE_CLASSES = [
        "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",  # 漲
        "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",  # 跌
        "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",  # 平盤
        "Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-down)",  # 跌停
        "Fz(32px) Fw(b) Lh(1) Mend(16px) C(#fff) Px(6px) Py(2px) Bdrs(4px) Bgc($c-trend-up)",  # 漲停
    ]

class Crawler:
    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def fetch_html(url: str) -> BeautifulSoup:
        response: Response = requests.get(url)
        response.raise_for_status()  # 檢查 HTTP 狀態碼
        return BeautifulSoup(response.text, "html5lib")

    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def crawl_price(stock_code:str) -> str:
        url:str = CrawlerConfig.BASE_URL.format(stock_code)
        soup:BeautifulSoup = Crawler.fetch_html(url)

        span_tag:Union[Tag, NavigableString, None] = soup.find('span', class_=lambda x: x and any(el in x for el in CrawlerConfig.PRICE_CLASSES))

        if isinstance(span_tag, Tag):
            price: str = span_tag.get_text().replace(",","")
            logger.info(f"[crawl_price] Get price = {price}")
            return price
        else:
            raise Exception(f"Fail to get {stock_code} price")

    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def crawl_lending(stock_code:str) -> list[str]:
        url:str = CrawlerConfig.LENDING_URL
        web:Response = requests.get(url)
        soup:BeautifulSoup = BeautifulSoup(web.text, "html5lib")
        trs:ResultSet = soup.find_all('tr', attrs={"align":"center", "style":"font-size:14px;"})

        # results = [balance_yest, selling_today, return_today, balance_today]
        results:list[str] = []

        for tr in trs:
            if tr.find('td').get_text() == str(stock_code):
                target_info = tr.find_all('td')

                for i in range(8, 13):
                    temp_data = target_info[i].get_text().replace(',', '')
                    results.append(cast(str, temp_data))

                break

        logger.info(f"[crawl_lending] Return {results}")
        
        return results

if __name__ == "__main__":
    try:
        Crawler.crawl_price(2454)
        Crawler.crawl_lending(2317)
    except requests.exceptions.RequestException as e:
        logger.error(f"[{__name__}] Network error: {e}")
    except AttributeError as e:
        logger.error(f"[{__name__}] Parsing error: {e}")
    except Exception as e:
        logger.error(f"[{__name__}] Exception: {e}")