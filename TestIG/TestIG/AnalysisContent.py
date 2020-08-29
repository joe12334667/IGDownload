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
                ans = client.topic(title, content)
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

        #計數，之後要拿掉       
        x += 1
        if x >= 100 :
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

    return hashtag_category    
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





#=============================================================================================================================================

print("連線至MongoDB中")
myclient = pymongo.MongoClient("mongodb+srv://joe12334667:joe12334667@captions.gjgzu.gcp.mongodb.net/captions?retrywrites=true&w=majority")
print("完成連線")
#database
db = myclient["Captions"]
#collection = sheet
collect = db["AllCaptions"]
for captions in collect.find({'$or':[ {'HashTag':"#動物園"}, {'HashTag':"#西門町"}, {'HashTag':"#炸雞"}, {'HashTag':"#美甲"}, {'HashTag':"#王俊凱"}, {'HashTag':"#王嘉爾"}, {'HashTag':"#健身"}]}):
    hashtag_category = baidu_nlp(captions["HashTag"] , captions["Allcaptions"])
    print(hashtag_category)
myclient = 0
