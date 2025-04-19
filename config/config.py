import  json
from typing import Optional


class ConfigManager:
    _instance:Optional["ConfigManager"] = None
    _config:dict = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open("./config/config.json", mode="r", encoding="utf-8") as file:
                cls._config = json.load(file)
            return cls._instance

    def get(self, key):
        return self._config.get(key)

if __name__ == "__main__":
    config = ConfigManager()

    stocks:dict = config.get("stock_code")

    for index, key in enumerate(stocks):
        print(key, stocks[key])