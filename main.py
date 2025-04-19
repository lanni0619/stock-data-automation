import module.stock
from config.config import ConfigManager
from module.stock import Stock

config = ConfigManager()

if __name__ == "__main__":
    stocks_dict:dict = config.get("stock_code")
    stocks:list["Stock"] = [Stock(key, stocks_dict[key]) for key in stocks_dict]

    for stock in stocks:
        stock.fetch_price()
        stock.fetch_lending()
        stock.save_to_excel()
        stock.plot_grid_price_ss()

        if stock.stock_code == "2317":
            stock.json_to_dc_stock()
            stock.image_to_dc_stock()