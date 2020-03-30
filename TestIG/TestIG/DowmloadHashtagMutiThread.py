import time
import threading
import queue
from datetime import datetime
from itertools import dropwhile, takewhile
import os
import csv
import json
from instaloader import Instaloader, Profile


#--------------------------------DownloadHashtagsFromCategory----------------------------------------------------------
def DownloadHashtagsFromCategory(HashTags , RunTime):
    HashTag = "#"+ HashTags

    # Get instance
    L = Instaloader(quiet=True, compress_json=False)

    AllHashTags = list()
    
    countRunTime = 0
    try:
        for post in L.get_hashtag_posts(HashTag[1:]):

            #沒有hashtags
            #因為當字符串或集合為空時，其值被隱式地賦為False。
            if not post.caption_hashtags :
                    continue

            countRunTime +=1
            #確認是否新增進HashTags
            for item in post.caption_hashtags:
                if is_all_chinese(item):
                    AllHashTags.append(item)
            #統計多少篇
            if countRunTime == RunTime :
               break
    except: 
        print("call too many api")
    #轉set以實現不重複陣列
    AllHashTags = set(AllHashTags)

    data = {"hashtags" : HashTag , "AllHashTags" : list(AllHashTags)}
    return data
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
# Worker 類別，負責處理資料
class Worker(threading.Thread):
    def __init__(self, queue , requeue , num ,work):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num
        self.requeue = requeue
        self.work = work
    def run(self):
        while self.queue.qsize() > 0:
            # 取得新的資料
            cat = self.queue.get()
            print("worker " , self.work , " ",cat)
            ReQueue.put( DownloadHashtagsFromCategory(cat , self.num) )
#--------------------------------------------------------------------------------------------------------------

tStart = time.time()
# 建立佇列
CatQueue = queue.Queue(0)
ReQueue = queue.Queue(0)
category = "食"
data = {category : []}

# 將資料放入佇列 
with open(os.getcwd() + "/" + "#"+category+".txt", newline='' , encoding="utf-8" ) as csvfile:

    # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    data = {category : []}
    #i = 0
  # 以迴圈輸出每一列
    for row in rows:
        for item in row:
            CatQueue.put(item)

# 建立兩個 Worker
my_worker1 = Worker(CatQueue, ReQueue ,  100 ,1)
my_worker2 = Worker(CatQueue, ReQueue , 100 , 2)

# 讓 Worker 開始處理資料
print("my_worker1 start")
my_worker1.start()
print("my_worker2 start")
my_worker2.start()

# 等待所有 Worker 結束
my_worker1.join()
my_worker2.join()


print("Done." )
while ReQueue.qsize() > 0:
    data[category].append(ReQueue.get())


FileName = time.strftime("%Y-%m-%d", time.localtime()) + category + ".json"

# 資料夾與檔案是否存在
if os.path.isfile(os.getcwd() + "/"+ category + "/" + FileName):
    file =open(os.getcwd() + "/"+ category + "/" + FileName , mode = 'w' , encoding="utf-8")
    print("檔案存在。")

else:
    if not os.path.isdir(os.getcwd() + "/"+ category):
        os.mkdir(category)
    file = open(os.getcwd() +"/" + category+ "/" + FileName , mode = 'w' , encoding="utf-8")
    print("檔案不存在，已創立" + FileName  )

# 寫入json檔並調整格式
file.write(json.dumps(data,ensure_ascii=False , indent=4, separators=(',', ': ')))
file.close()
    
tEnd = time.time()
print("time : %f s" % (tEnd - tStart))
