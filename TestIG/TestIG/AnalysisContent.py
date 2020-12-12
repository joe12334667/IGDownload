import pymongo
import json
from pprint import pprint
from aip import AipNlp
import pprint
import queue
import time
import pandas as pd
import os
import csv
import re
import json

def baidu_nlp(title , contents , ReQueue):

    #https://ai.baidu.com/ai-doc/NLP/tk6z52b9z#%E6%96%87%E7%AB%A0%E5%88%86%E7%B1%BB
    #""" 你的 APPID AK SK """
    APP_ID = '21859116'
    API_KEY = '59ENG3lpaaO2twkZoswNZV95'
    SECRET_KEY = 'xY6TSzna5T4as0VLCdZoyT74r1tw9sKx'
    print("連線百度雲中")
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    print("連線完成")
    title = title.replace("#" , "")
    print(title)
    i = 0
    x = 0
    content_df = pd.DataFrame()
    ans = ''
    for content in contents:
        
        #每秒NLP限制存取2次，故設定跑2次睡幾秒
        if i >= 2:
            #print("sleep")
            time.sleep(1)
            i = 0
        else :
            i = i + 1

        #用迴圈保證每個content不會因為呼叫過快傳回error code而沒被計算
        
        y = True
        while y:
            try : 
                #調用文章分類
                ans = client.topic(title, content['captions'])
                pprint.pprint(ans)
                content_df = content_df.append(ans['item']['lv1_tag_list'],ignore_index=True)
                y = False
            except : 
                pprint.pprint(ans)
                if ans == '':
                    print("空白")
                    y = False
                    continue
                if ans.__contains__('error_code') :
                    if ans['error_code'] == 18:
                        print("wait 1s")
                        time.sleep(1)
                        continue
                    if ans['error_code'] == 282134 :
                        y = False
                        continue

                y = False

                #print("except")
            if ans['item']['lv1_tag_list'][0]['tag']== title:
                data = {"HashTag" : title , "AllHashTags" : list(content['hashtags']) }
                ReQueue.put(data);
        #計數，之後要拿掉       
        x += 1
        if x >= 10 :
            break

    hashtag_category = []
    tag_group = content_df.groupby("tag")
    print("hashtag : " , title)
    print("all:" , content_df.loc[:,['tag']].size)
    for group_name, group_data in tag_group:#都是DataFrame的型態
        print("tag: " , group_name)
        print("tag_count: " , group_data.loc[:,['tag']].size)
        
        #.loc[:,['tag']] => 選取不指定index中，columns指定為tag的資料
        if (group_data.loc[:,['tag']].size / content_df.loc[:,['tag']].size) >= 0.4 :
            hashtag_category.append(group_name)

    return ReQueue    
    #print("class \n" ,content_df)
    
    #print(content_df.shape) # 回傳列數與欄數  
    #print("---")  
    #print(content_df.describe()) # 回傳描述性統計  
    #print("---")  
    ##print(content_df.head(3)) # 回傳前三筆觀測值  
    ##print("---")  
    ##print(content_df.tail(3)) # 回傳後三筆觀測值  
    ##print("---")  
    ##print(content_df.columns) # 回傳欄位名稱  
    ##print("---")  
    ##print(content_df.index) # 回傳 index  
    ##print("---")  
    #print(content_df.info) # 回傳資料內容 
    #print("---")  
    #print(tag_group) # 各組的人數  
    #pprint.pprint(list(tag_group))






def WriteHashTagsJson(data):
    FileName = time.strftime("%Y-%m-%d_%H-%M-%S")  + ".json"

    # 資料夾與檔案是否存在
    if os.path.isfile(os.getcwd() + "/"+ "HashTags" + "/" + FileName):
        file =open(os.getcwd() + "/"+ "HashTags" + "/" + FileName , mode = 'w' , encoding="utf-8")
        print("檔案存在。")

    else:
        if not os.path.isdir(os.getcwd() + "/"+ "HashTags"):
            os.mkdir("HashTags")
        file = open(os.getcwd() +"/" + "HashTags"+ "/" + FileName , mode = 'w' , encoding="utf-8")
        print("檔案不存在，已創立" + FileName  )

    # 寫入json檔並調整格式
    file.write(json.dumps(data,ensure_ascii=False , indent=4, separators=(',', ': ')))
    file.close()

    FileName =  "HashTags_done.json"
    HashTags_done = list()
    #寫 HashTags_done.json
    # 資料夾與檔案是否存在
    if os.path.isfile(os.getcwd() +  "/" + FileName):
            file =open(os.getcwd() +  "/" + FileName , mode = 'r' , encoding="utf-8")
            print("檔案存在。" , FileName)

    else:
        file = open(os.getcwd() +"/" + FileName , mode = 'r' , encoding="utf-8")
        print("檔案不存在，已創立" + FileName  )



    
    json_array = json.load(file)

    for items in json_array["HashTags"]:
        HashTags_done.append(items)

    file.close()
    
    file =open(os.getcwd() +  "/" + FileName , mode = 'w' , encoding="utf-8")

    for HashTags in  data["HashTags"]:
        HashTags_done.append(HashTags["HashTag"][1:])
    # 寫入json檔並調整格式
    file.write(json.dumps( {"HashTags" : list(HashTags_done)} ,ensure_ascii=False , indent=4, separators=(',', ': ')))
    file.close()
#=============================================================================================================================================

print("連線至MongoDB中")
myclient = pymongo.MongoClient("mongodb+srv://joe12334667:joe12334667@captions.gjgzu.gcp.mongodb.net/captions?retrywrites=true&w=majority")
print("完成連線")
#database
db = myclient["Captions"]
#collection = sheet
collect = db["AllCaptions"]
cats = {"健康養生",
		"動漫",
		"國際",
		"娛樂",
		"家居",
		"寵物",
		"情感",
		"搞笑",
		"教育",
		"旅遊",
		"文化",
		"歷史",
		"汽車",
		"星座運勢",
		"社會",
		"科技",
		"育兒",
		"財經",
		"時事",
		"時尚",
		"遊戲",
		"綜合",
		"美食",
		"音樂",
		"體育",
		"軍事"}
ReQueue = queue.Queue(0)
for cat in cats:
    for captions in collect.find({'$or':[ {'HashTag':"#" + cat}]}):
        hashtag_category = baidu_nlp(cat , captions["Allcaptions"] , ReQueue )
        print(hashtag_category)
    
data = {"HashTags" : []}
data["HashTags"].append(ReQueue.get())
WriteHashTagsJson(data)
myclient = 0
