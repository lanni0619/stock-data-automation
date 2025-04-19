# 3rd party package
import requests
from requests import Response
# apscheduler don't have official stub

# Standard module
from datetime import datetime
import os
from typing import Optional

# Custom module
from module.logger import logger
import module.utils as utils


# Config: Discord_Stock_Channel_Config
class Config:
    BASE_URL:str = "https://discord.com/api/webhooks/1356484738029719573/9GNCPHfl7gcz9BpkkO1xYEYqZ9_D2tWd0dx5sZqx3RTN3HgLFLql47TEgWYEsz0Q4x8g"
    
    # SEND JSON, {0}=json_data
    JSON_HEADERS:dict = {"Content-Type": "application/json"}
    JSON_PAYLOAD:dict = {"content": "content", "username": "newmanBot"}

    # SEND IMG
    IMG_PAYLOAD:dict = {"username": "newmanBot"}
    # {0}=stock_code, {1}=YY-MM
    IMG_PATH:str = "C:/temp/stock-log/{0}_{1}.jpg"

class DcStockChannel:
    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def send_json(o:dict) -> None:
        url = Config.BASE_URL
        headers = Config.JSON_HEADERS
        payload = Config.JSON_PAYLOAD
        o_json = utils.dict_to_json(o)
        payload["content"] = o_json
        
        # Send data to discord
        res:Response = requests.post(url, headers = headers, json = payload)
        logger.info("[send_json] successfully")

    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def send_image(stock_code:str) -> None:
        img_file_path:Optional[str] = DcStockChannel._is_file_exist(stock_code)

        if img_file_path:
            files = {'media': open(img_file_path, 'rb')}
            requests.post(Config.BASE_URL, data=Config.IMG_PAYLOAD, files=files)
            logger.info("[send_image] successfully")
        else:
            logger.warning("[send_chart] Image file is not exist!")

    @staticmethod
    def _is_file_exist(stock_code:str) -> Optional[str]:
        yy_mm = datetime.now().strftime('%Y-%m')
        img_file_path = Config.IMG_PATH.format(stock_code, yy_mm)
        logger.info(f"[_is_file_exist] img_file_path={img_file_path}")

        if not os.path.exists(img_file_path):
            return None
        return img_file_path

if __name__ == "__main__":
    A = {"name":"roy", "age":100}
    # send_json
    DcStockChannel.send_json(A)

    # send_image
    DcStockChannel.send_image("2317")