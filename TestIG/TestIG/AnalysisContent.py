import pymongo
import json
from pprint import pprint
from aip import AipNlp
import pprint
import time
import pandas as pd

def baidu_nlp(title , contents):

    #https://ai.baidu.com/ai-doc/NLP/tk6z52b9z#%E6%96%87%E7%AB%A0%E5%88%86%E7%B1%BB
    #""" 你的 APPID AK SK """
    APP_ID = '21859116'
    API_KEY = '59ENG3lpaaO2twkZoswNZV95'
    SECRET_KEY = 'xY6TSzna5T4as0VLCdZoyT74r1tw9sKx'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    title = title.replace("#" , "")
    i = 0
    x = 0
    content_df = pd.DataFrame()
    for content in contents:
        x += 1
        if i >= 2:
            #print("sleep")
            time.sleep(3)
            i = 0
        else :
            i = i + 1

        #""" 调用文章分类 """
        ans = client.topic(title, content)
        pprint.pprint(ans)
        try : 
            content_df = content_df.append(ans['item']['lv1_tag_list'],ignore_index=True)
        except : 
            print("except")
            continue
        if x >= 10 :
            break
    
    print("class \n" ,content_df)
    
    print(content_df.shape) # 回傳列數與欄數  
    print("---")  
    print(content_df.describe()) # 回傳描述性統計  
    print("---")  
    print(content_df.head(3)) # 回傳前三筆觀測值  
    print("---")  
    print(content_df.tail(3)) # 回傳後三筆觀測值  
    print("---")  
    print(content_df.columns) # 回傳欄位名稱  
    print("---")  
    print(content_df.index) # 回傳 index  
    print("---")  
    print(content_df.info) # 回傳資料內容 
    print("---")  
    print(content_df.groupby("tag").size()) # 各組的人數  


myclient = pymongo.MongoClient("mongodb+srv://joe12334667:joe12334667@captions.gjgzu.gcp.mongodb.net/captions?retrywrites=true&w=majority")
#database
db = myclient["Captions"]
#collection = sheet
collect = db["AllCaptions"]
for obj in collect.find().limit(1):
    baidu_nlp(obj["HashTag"] , obj["Allcaptions"])
    

