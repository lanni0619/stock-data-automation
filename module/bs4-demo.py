import requests
from bs4 import BeautifulSoup

url = 'https://water.taiwanstat.com/'
web = requests.get(url)                        # 取得網頁內容
# soup = BeautifulSoup(web.text, "html.parser")  # 轉換成標籤樹 html.parser 容錯率比html5lib高，但速度較快
soup = BeautifulSoup(web.text, "html5lib") # 安裝模組即可使用，不需要import

reservoirs = soup.find_all('div', class_='reservoir')
print(reservoirs)
for reservoir in reservoirs:
    print(reservoir.find('h3').get_text(), end=" ")
    print(reservoir.find('h5').get_text())