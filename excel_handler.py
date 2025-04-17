# 3rd-party
import openpyxl
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

# standard
from datetime import datetime
from os import path
from typing import Union, Optional, cast
import traceback

# self-define
import utils

class ExcelHandler:
    # 0=stock_code, 1=YY-MM
    FILE_PATH = path.join("C:/temp/stock-log", "{0}_{1}.xlsx")
    INSTANCE_CACHE:dict = {}

    def __init__(self, wb=Workbook, sheet=Worksheet):
        self.wb = wb
        self.sheet = sheet

    @classmethod
    @utils.tic_tok
    @utils.handle_errors
    def check_or_create_file(cls, stock_code:int) -> Optional[object]:
        yy_mm = datetime.today().strftime('%Y-%m')
        file_path = cls.FILE_PATH.format(stock_code, yy_mm)

        if cls.INSTANCE_CACHE.get(file_path, None) == None:
            wb:Workbook = openpyxl.load_workbook(file_path, data_only=True) if path.exists(file_path) else Workbook()
            sheet:Worksheet = cast(Worksheet, wb.active)
            cls.INSTANCE_CACHE[file_path] = True
            return cls(wb, sheet)
        else:
            return None

    @staticmethod
    def initialize_sheet():
        pass

    @staticmethod
    def append_row():
        pass

    @staticmethod
    def read_last_row():
        pass

    @staticmethod
    def is_duplicate():
        pass

    @staticmethod
    def save_file():
        pass

if __name__ == "__main__":
    try:
        # Testing duplicate file
        excel_2317 = ExcelHandler.check_or_create_file(2317)
        excel_2330 = ExcelHandler.check_or_create_file(2317)
        print(excel_2317, excel_2330) # object, None
    except Exception as e:
        traceback.print_exc()
        print(e)

# def save_to_excel(self) -> None:
#     try:
#         logger.info(f"save_to_excel - stock_number = {self._stock_code}")

#         # 1) Preliminary
#         today:datetime = datetime.today()
#         root_path:str = "C:/temp/stock-log"
#         filename:str = os.path.join(root_path, f"{self._stock_code}_{today.strftime('%Y-%m')}.xlsx")
#         attrs:list[str] = ["created_at", "balance_yest", "selling_today", "return_today", "balance_today", "price"]

#         wb = openpyxl.load_workbook(filename, data_only=True) if os.path.exists(filename) else Workbook()
#         sheet:Worksheet = cast(Worksheet, wb.active)

#         # 2) Check if data exist ?
#         if os.path.exists(filename):
#             logger.info(f"save_to_excel - file exists")
#             # Get max_row number which is the index of latest record
#             max_row:int = sheet.max_row
#             if max_row != 1:
#                 # Get last record datetime (string, yyyy-mm-dd)
#                 # cast(type, val) => Tell mypy the type of val
#                 lr_date:str = cast(str, sheet.cell(max_row, 1).value)[0:10]

#                 # 3) Check if data duplicate ?
#                 if lr_date == today.strftime("%Y-%m-%d"):  # compare with today
#                     logger.info("save_to_excel - Duplicate date of record, stop saving data ")
#                     return

#         # 4) if file not exists
#         else:
#             logger.info(f"save_to_excel - file not exists, creating ...")
#             sheet.append(attrs)
#             wb.save(filename)

#         # 5) build new row
#         logger.info(f"save_to_excel - Building new row ...")
#         row_arr:list[Union[str, float]] = []
#         for attr in attrs:
#             value:str = getattr(self, "_"+attr)
#             if attr != "created_at" and value is not None:
#                 row_arr.append(float(value.replace(",", "")))
#             elif attr == "created_at":
#                 row_arr.append(value)
#             else:
#                 row_arr.append("")

#         sheet.append(row_arr)
#         wb.save(filename)

#         logger.info("save_to_excel - finish")

#     except Exception as e:
#         print(e)