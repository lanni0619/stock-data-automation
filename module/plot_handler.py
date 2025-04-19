# 3rd-party package
import matplotlib # type: ignore
import matplotlib.pyplot as plt # type: ignore

# Standard
from os import path

# Self-define
import module.utils as utils
from config.config import config

matplotlib.use("Agg")

class PlotHandler:
    @staticmethod
    @utils.tic_tok
    @utils.handle_errors
    def plot_grid(data_x:list, data_y:list, info_dict:dict) -> None:
        """ data_y = [[data1], [data2], ...] """
        GRID_WIDTH = 10
        GRID_HEIGHT = 5

        plt.figure(figsize=(GRID_WIDTH, GRID_HEIGHT))
        for index, data in enumerate(data_y):
            label = "short selling (unit - 1k lot)" if index == 0 else "price (unit - NTD)"
            plt.plot(data_x, data, label=label)

        plt.xlabel("date")
        plt.ylabel("shares")
        plt.title(f"{info_dict['stock_code']} - PRICE VS SHORT SELLING")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()

        yy_mm = info_dict["update_time"][0:7]

        path_name = config.get("image_settings")["root_path"].format(info_dict["stock_code"])
        img_name = config.get("image_settings")["file_name"].format(info_dict['stock_code'], yy_mm)

        save_path = path.join(path_name, img_name)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()

if __name__ == "__main__":
    print(config.get("image_settings")["root_path"])
    print(config.get("image_settings")["file_name"])