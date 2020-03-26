from datetime import datetime
from itertools import dropwhile, takewhile
import time
import os
import csv
from instaloader import Instaloader, Profile


#--------------------------------DownloadHashtagsFromCategory----------------------------------------------------------
def DownloadHashtagsFromCategory(HashTags , category):
    HashTag = "#"+ HashTags
    FileName =  HashTags + ".txt"

    #資料夾與檔案是否存在
    if os.path.isfile(os.getcwd() + "/"+ category + "/" + FileName):
        file =open(os.getcwd() + "/"+ category + "/" + FileName , mode = 'a+' , encoding="utf-8")
        print("檔案存在。")

    else:
        if not os.path.isdir(os.getcwd() + "/"+ category):
            os.mkdir(category)
        file = open(os.getcwd() +"/" + category+ "/" + FileName , mode = 'w' , encoding="utf-8")
        print("檔案不存在，已創立" + FileName  )


    #計時開始
    tStart = time.time()


    # Get instance
    L = Instaloader(quiet=True, compress_json=False)

    AllHashTags = list()
    
    i = 0
    count_likes = 0
    for post in L.get_hashtag_posts(HashTag[1:]):

        if not post.caption_hashtags :
            #因為當字符串或集合為空時，其值被隱式地賦為False。
                print ("pass")
                print("hashtags : " , post.caption_hashtags)
                continue
        i+=1
        print(i , ":" , post.likes)
        print("hashtags : " , post.caption_hashtags)
        count_likes+=post.likes

        #確認是否新增進HashTags
        for item in post.caption_hashtags:
            if is_all_chinese(item):
                AllHashTags.append(item)
        
        #L.download_post(post, target=profile.username)

        #統計多少篇
        if i==100 :
           break

    print("total ig likes : " , count_likes )
    AllHashTags = set(AllHashTags)
    print("All HashTags : " ,  AllHashTags  )
    count = 0
    #寫檔
    for hashtag in AllHashTags:
        if(count != 0):
            file.write(",")
        file.write(hashtag)
        count+=1
    print(count)
    file.close()

    tEnd = time.time()

    print("time : %f s" % (tEnd - tStart))


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

with open(os.getcwd() + "/" + "#衣.txt", newline='' , encoding="utf-8" ) as csvfile:

  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)

  # 以迴圈輸出每一列
  for row in rows:
    for item in row:
        print(item)
        DownloadHashtagsFromCategory(item , "衣")





