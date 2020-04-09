import time
import threading
import queue
from datetime import datetime
from itertools import dropwhile, takewhile
import os
import csv
import re
import json
from instaloader import Instaloader, Profile


categorys = ["食" , "衣" , "住" , "行" ]
AllHashTags = []

for category in categorys:
    with open(os.getcwd() + "/" + "#"+category+".txt", newline='' , encoding="utf-8" ) as csvfile:

            # 讀取 CSV 檔案內容
            rows = csv.reader(csvfile)
            data = {category : []}
            #i = 0
          # 以迴圈輸出每一列
            for row in rows:
                for item in row:
                    AllHashTags.append(item)

FileName =  "HashTags.json"

# 資料夾與檔案是否存在
if os.path.isfile(os.getcwd() +  "/" + FileName):
    file =open(os.getcwd() +  "/" + FileName , mode = 'w' , encoding="utf-8")
    print("檔案存在。")

else:
    if not os.path.isdir(os.getcwd() ):
        os.mkdir(category)
    file = open(os.getcwd() +"/" + FileName , mode = 'w' , encoding="utf-8")
    print("檔案不存在，已創立" + FileName  )

data = {"HashTags" : AllHashTags }
# 寫入json檔並調整格式
file.write(json.dumps( data ,ensure_ascii=False , indent=4, separators=(',', ': ')))
file.close()
    
