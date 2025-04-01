import openpyxl
import matplotlib.pyplot as plt

# 讀取 Excel 檔案
wb = openpyxl.load_workbook("mock_data.xlsx")
ws = wb.active

# 讀取資料（假設第一列是標題，數據從第二列開始）
time = []
data_series = [[] for _ in range(4)]  # 假設有 4 個數據欄位

for row in ws.iter_rows(min_row=2, values_only=True):
    time.append(row[0])  # 第一欄是時間
    for i in range(4):
        data_series[i].append(row[i+1])  # 其他欄是數據

# 繪製圖表
plt.figure(figsize=(10, 5))
for i, data in enumerate(data_series):
    plt.plot(time, data, label=f"Series {i+1}")

plt.xlabel("Time")
plt.ylabel("Values")
plt.title("Excel Data Plot")
plt.legend()
plt.xticks(rotation=45)
plt.grid()

# 儲存為 JPG
plt.savefig("chart.jpg", dpi=300, bbox_inches="tight")
plt.show()