import pandas as pd
import os
import sys

columns = ['LOG_STATUS', 'MESSAGE']
df = pd.DataFrame(columns=columns, )

text = "ERROR LOG: \nSUCCESS LOG: "

root_path = sys.path[0]
print(root_path)
file_path = os.path.join(root_path, "log", "file.txt")
print(file_path)

with open(file_path, 'a') as file:
    file.write('ERROR: log messaging error\n')
    file.write('SUCCESS: log messaging success\n')

with open(file_path, 'r') as file:
    for line in file.readlines():
        line = line.strip()
        if 'ERROR' in line:
            df2 = pd.Series({'LOG_STATUS': 'ERROR', 'MESSAGE': line})
        elif 'SUCCESS' in line:
            df2 = pd.Series({'LOG_STATUS': 'SUCCESS', 'MESSAGE': line})
        df = pd.concat([df, df2], ignore_index=True)[columns]

print(df)

df.to_csv('file_name.csv', encoding='utf-8')