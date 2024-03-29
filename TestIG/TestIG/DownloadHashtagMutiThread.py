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
import requests
from lxml.html import fromstring
from itertools import cycle
import traceback


#--------------------------------DownloadHashtagsFromCategory----------------------------------------------------------
def DownloadHashtagsFromCategory(HashTags , RunTime):
    HashTag = "#"+ HashTags
    lock = threading.Lock() 
    # Get instance
    L = Instaloader(quiet=True, compress_json=False , max_connection_attempts = 10)

    AllHashTags = list()
    
    countRunTime = 0
    lock.acquire() 
    posts = L.get_hashtag_posts(HashTags)
    lock.release()
    try:
        for post in posts :

            #沒有hashtags
            #因為當字符串或集合為空時，其值被隱式地賦為False。
            if not post.caption_hashtags :
                    continue

            countRunTime +=1
            #確認是否新增進HashTags
            for item in post.caption_hashtags:
                if is_all_chinese_And_English(item):
                    AllHashTags.append(item)
            #統計多少篇
            if countRunTime == RunTime :
                break
    except Exception as e:
        print("except:" , e)
    #轉set以實現不重複陣列
    AllHashTags = set(AllHashTags)

    data = {"HashTag" : HashTag , "AllHashTags" : list(AllHashTags) , "Time" : time.strftime("%Y-%m-%d_%H-%M-%S")}
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

def is_all_chinese_And_English(strs):
    ret_search = re.search("^[\u4e00-\u9fa5_a-zA-Z0-9\-]+$",strs) #掃描整個字串返回第一個匹配到的元素並結束，匹配不到返回None
    if(ret_search):
        return True
    return False


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
            HashTag = self.queue.get()
            print("worker " , self.work , " ",HashTag)
            self.requeue.put( DownloadHashtagsFromCategory(HashTag , self.num) )



class WorkerIncludeDownload(threading.Thread):
    def __init__(self, queue , requeue , data , num ,work):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num
        self.requeue = requeue
        self.work = work
        self.data = data
        #執行緒鎖
        self.lock = threading.Lock()
        self.data = data
    def run(self):
        while self.queue.qsize() > 0:
            # 取得新的資料
            HashTag = self.queue.get()
            print("worker " , self.work , " ",HashTag)
            self.requeue.put( DownloadHashtagsFromCategory(HashTag , self.num))

            if self.requeue.qsize() >= 100 :
                #鎖定資源 不讓其他執行緒跑
                if self.lock.acquire():
                    print("Lock Thead and output json")
                    while self.requeue.qsize() > 0:
                        self.data["HashTags"].append(self.requeue.get())
                    WriteHashTagsJson(self.data)
                    self.data["HashTags"].clear()
                    self.lock.release()

#-----------------------------------------------MutiTheadDownloadByCategory---------------------------------------------------------------

def MutiTheadDownloadByCategory(cate , RunTime):

    tStart = time.time()
    # 建立佇列
    CatQueue = queue.Queue(0)
    ReQueue = queue.Queue(0)
    category = cate
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


   

    
   
    while CatQueue.qsize() > 0:

        # 建立兩個 Worker
        my_worker1 = Worker(CatQueue, ReQueue , RunTime , 1)
        my_worker2 = Worker(CatQueue, ReQueue , RunTime , 2)

        # 讓 Worker 開始處理資料
        print("my_worker1 start")
        my_worker1.start()
        time.sleep(3)
        print("my_worker2 start")
        my_worker2.start()
        # 等待所有 Worker 結束
        my_worker1.join(60)
        my_worker2.join(60)


    print("Done." )
    while ReQueue.qsize() > 0:
        data[category].append(ReQueue.get())


    FileName = time.strftime("%Y-%m-%d_%H-%M") + category + ".json"

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



#-------------------------------------------DownloadAllHashTags-----------------------------------------------------------

def DownloadAllHashTags(RunTime):
    tStart = time.time()
    # 建立佇列
    HashTagQueue = queue.Queue(0)
    ReQueue = queue.Queue(0)
    data = {"HashTags" : []}
    fileName = "HashTags.json"
    HashTags = list()
    HashTags_done = list()

    # 將資料放入佇列 
    with open(os.getcwd() + "/" + fileName , mode = 'r' , encoding="utf-8") as file:

        json_array = json.load(file)

        for item in json_array["HashTags"]:
            HashTags.append(item)
            
    with open(os.getcwd() + "/" + "HashTags_done.json" , mode = 'r' , encoding="utf-8") as file:

        json_array = json.load(file)

        for item in json_array["HashTags"]:
            HashTags_done.append(item)
            
    if not list(set(HashTags) - set(HashTags_done)) :
        for item in HashTags:
            HashTagQueue.put(item)
            print("HashTags_done is emply")
            file =open(os.getcwd() +  "/" + "HashTags_done.json" , mode = 'w' , encoding="utf-8")
            # 寫入json檔並調整格式
            file.write(json.dumps( {"HashTags" : list()} ,ensure_ascii=False , indent=4, separators=(',', ': ')))
            file.close()

    else:
        print("HashTags - HashTags_done")
        items = list(set(HashTags) - set(HashTags_done))
        for item in sorted( items) :
            HashTagQueue.put(item)
            

    i = 0
    time_start = time.time()
    try :
        while HashTagQueue.qsize() > 0:
            
            if  i >= 10 :
                print("-" * 30 )
                print("wait for 30 mins")
                print("-" * 30 )
                time.sleep(1800)
                i = 1
            else : 
                i += 1
            print("i = " ,i)

            # 建立兩個 Worker
            #WorkerIncludeDownload 包含每抓完一百的HashTags,自動寫成JSON
            my_worker1 = WorkerIncludeDownload(HashTagQueue, ReQueue , data , RunTime , 1)
            my_worker2 = WorkerIncludeDownload(HashTagQueue, ReQueue , data , RunTime , 2)

            # 讓 Worker 開始處理資料
            print("my_worker1 start")
            my_worker1.start()
            time.sleep(3)
            print("my_worker2 start")
            my_worker2.start()
            # 等待所有 Worker 結束
            #生命週期60s
            my_worker1.join(60)
            my_worker2.join(60)

    except:
        switch_proxy()

    print("Done." )
    i = 0
    
    while ReQueue.qsize() > 0:

        data["HashTags"].append(ReQueue.get())
        i+=1
        #100個HashTags後寫檔
        if i>= 100 :
            WriteHashTagsJson(data)
            #清除list
            data["HashTags"].clear()
            i = 0

    #最後少於100個時寫檔
    if ReQueue.qsize() <= 0 and data["HashTags"] :
        WriteHashTagsJson(data)
        data["HashTags"].clear()


    tEnd = time.time()
    print("time : %f s" % (tEnd - tStart))
    


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



def switch_proxy():
        
        proxy = get_proxies()
        # proxy = 'host:port'
        os.environ['https_proxy'] = proxy

def get_proxies():
    while True:
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)

        proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                #Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)

        url = 'https://httpbin.org/ip'
        print(proxies)
        proxy_pool = cycle(proxies)
        for i in range(1,10):
            #Get a proxy from the pool
            proxy = next(proxy_pool)
            print("Request #%d"%i)
            print(proxy)
            try:
                response = requests.get(url,proxies={"http": proxy, "https": proxy},timeout = 10)
                print(response.json())
                print("break")
                return proxy


            except:
                #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
                #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
                print("Skipping. Connnection error")


DownloadAllHashTags(100)