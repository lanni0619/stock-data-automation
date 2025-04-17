# 3rd party package
import requests
from requests import Response
# apscheduler don't have official stub

# Standard module
import json
from datetime import datetime
import os
from typing import Any, Callable, Optional, Union, cast

# Custom module
from module.plot import plot_short_selling
from logger import logger
import utils

# StockChannelCfg: Discord_Stock_Channel_Config
class StockChannelCfg:
    BASE_URL:str = "https://discord.com/api/webhooks/1356484738029719573/9GNCPHfl7gcz9BpkkO1xYEYqZ9_D2tWd0dx5sZqx3RTN3HgLFLql47TEgWYEsz0Q4x8g"
    
    # SEND JSON, {0}=json_data
    JSON_HEADERS:dict = {"Content-Type": "application/json"}
    JSON_PAYLOAD:dict = {"content": "content", "username": "newmanBot"}

    # SEND IMG, {0}=filename.jpg, {1}=bufferedReader
    IMG_FILE:dict = {"file": ({0}, {1}, "image/jpeg")}
    IMG_PAYLOAD:dict = {"username": "newmanBot"}
    # {0}=stock_code, {1}=YY-MM
    IMG_PATH:str = f"C:/temp/stock-log/{0}_{1}.jpg"

class StockChannel:
    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def send_json(o) -> None:
        if not all(getattr(o, attr) is not None for attr in vars(o)):
            logger.error("[send_json] - data incomplete")
            return None
        
        json_str:str = utils.json_stringify(o)
        url = StockChannelCfg.BASE_URL
        headers = StockChannelCfg.JSON_HEADERS
        payload = StockChannelCfg.JSON_PAYLOAD
        payload["content"] = json_str
        
        # Send data to discord
        res:Response = requests.post(url, headers = headers, json = payload)
        logger.info("[send_json] - successfully")

    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def send_chart():
        pass

# def send_chart(self) -> None:
#     logger.info(f"send_chart - stock_number = {self._stock_code}")
#     # 1) draw new chart
#     plot_short_selling(self._stock_code)

#     # 2) Path to the JPG file
#     today:datetime = datetime.today()
#     jpg_file_path:str = f"C:/temp/stock-log/{self._stock_code}_{today.strftime('%Y-%m')}.jpg"  # Replace with your actual file name

#     # 3) Discord webhook URL
#     url:str = "https://discord.com/api/webhooks/1356484738029719573/9GNCPHfl7gcz9BpkkO1xYEYqZ9_D2tWd0dx5sZqx3RTN3HgLFLql47TEgWYEsz0Q4x8g"

#     # 4) Check if the file exists
#     if not os.path.exists(jpg_file_path):
#         logger.info(f"send_chart - File not found: {jpg_file_path}")
#         return

#     # 5) Prepare the file and payload
#     with open(jpg_file_path, "rb") as file:
#         files:dict = {"file": (os.path.basename(jpg_file_path), file, "image/jpeg")}
#         payload:dict = {"username": "newmanBot"}

#         # Send the request
#         res = requests.post(url, data=payload, files=files)

#     # 6) Read the response
#     if res.status_code in (200, 204):
#         logger.info(f"send_chart - success")
#     else:
#         logger.info(f"send_chart - fail")

if __name__ == "__main__":
    class Person:
        def __init__(self):
            self.name = "roy"
            self.age = 100
    
    A = Person()

    StockChannel.send_json(A)