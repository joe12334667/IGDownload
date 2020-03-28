from datetime import datetime
from itertools import dropwhile, takewhile
import time
import os
import csv
import json
from instaloader import Instaloader, Profile


#--------------------------------DownloadHashtagsFromCategory----------------------------------------------------------
def DownloadHashtagsFromCategory(HashTags , RunTime):
    HashTag = "#"+ HashTags
    FileName =  HashTags + ".json"

    ##資料夾與檔案是否存在
    #if os.path.isfile(os.getcwd() + "/"+ category + "/" + FileName):
    #    file =open(os.getcwd() + "/"+ category + "/" + FileName , mode = 'a+' , encoding="utf-8")
    #    print("檔案存在。")

    #else:
    #    if not os.path.isdir(os.getcwd() + "/"+ category):
    #        os.mkdir(category)
    #    file = open(os.getcwd() +"/" + category+ "/" + FileName , mode = 'w' , encoding="utf-8")
    #    print("檔案不存在，已創立" + FileName  )


    #計時開始
    #tStart = time.time()


    # Get instance
    L = Instaloader(quiet=True, compress_json=False)

    AllHashTags = list()
    
    i = 0
    count_likes = 0
    for post in L.get_hashtag_posts(HashTag[1:]):

        if not post.caption_hashtags :
            #沒有hashtags
            #因為當字符串或集合為空時，其值被隱式地賦為False。
                #print ("pass")
                #print("hashtags : " , post.caption_hashtags)
                continue

        i+=1
        #print(i , ":" , post.likes)
        #print("hashtags : " , post.caption_hashtags)
        count_likes+=post.likes

        #確認是否新增進HashTags
        for item in post.caption_hashtags:
            if is_all_chinese(item):
                AllHashTags.append(item)
        
        #L.download_post(post, target=profile.username)

        #統計多少篇
        if i== RunTime :
           break

    #print("total ig likes : " , count_likes )
    #轉set以實現不重複陣列
    AllHashTags = set(AllHashTags)
    #print("All HashTags : " ,  AllHashTags  )
    data = {"hashtags" : HashTag , "AllHashTags" : list(AllHashTags)}
    return data

    #count = 0
    #data["AllHashTags"] = list(AllHashTags)
    #寫檔
    #for hashtag in AllHashTags:
    #    if(count != 0):
    #        file.write(",")
    #    file.write(hashtag)
    #    count+=1

    #file.write(json.dumps(data,ensure_ascii=False))
    
    #print(count)
    #file.close()

    #tEnd = time.time()

    #print("time : %f s" % (tEnd - tStart))


#--------------------------------DownloadHashtagsFromCategory----------------------------------------------------------
#--------------------------------is_contains_chinese----------------------------------------------------------
#是否中文
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True
#--------------------------------is_contains_chinese----------------------------------------------------------


#計時開始
tStart = time.time()
category = "食"
with open(os.getcwd() + "/" + "#"+category+".txt", newline='' , encoding="utf-8" ) as csvfile:

    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    data = {category : []}
    #i = 0
  # 以迴圈輸出每一列
    for row in rows:
        for item in row:
            #i+=1
            #print(i)

            print(item)
            data[category].append(DownloadHashtagsFromCategory(item , 100))
            #DownloadHashtagsFromCategory(item)
            #if(i==2):
            #    break
    FileName = time.strftime("%Y-%m-%d", time.localtime()) + category + ".json"
    print(json.dumps(data,ensure_ascii=False))
        #資料夾與檔案是否存在
    if os.path.isfile(os.getcwd() + "/"+ category + "/" + FileName):
        file =open(os.getcwd() + "/"+ category + "/" + FileName , mode = 'w' , encoding="utf-8")
        print("檔案存在。")

    else:
        if not os.path.isdir(os.getcwd() + "/"+ category):
            os.mkdir(category)
        file = open(os.getcwd() +"/" + category+ "/" + FileName , mode = 'w' , encoding="utf-8")
        print("檔案不存在，已創立" + FileName  )

    file.write(json.dumps(data,ensure_ascii=False , indent=4, separators=(',', ': ')))
    file.close()

    tEnd = time.time()
    print("time : %f s" % (tEnd - tStart))

