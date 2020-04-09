import pymongo
import json
import os
import time
import shutil 
from os import listdir
from pprint import pprint


def WriteAllHashTagsToMongoDB():

    category = "HashTags"
    newHashTags = []
    oldHashTags = []
    FileName =  "HashTags.json"

    #抓出資料夾所有的檔案
    files = listdir(os.getcwd() + "/"+ "HashTags")
    #pprint(files)
    dir =  "MongoDB_" + time.strftime("%Y-%m-%d_%H-%M") + category

    for fileName in files:
        #不要資料夾
        if os.path.isdir(os.getcwd() + "/"+ category + "/" +fileName):
            continue
        #開檔
        file =open(os.getcwd() + "/"+ category + "/" + fileName , mode = 'r' , encoding="utf-8")
        json_array = json.load(file)

        for items in json_array[category]:
            #print(items["hashtags"] , end =" , ")
            #pprint(items["allhashtags"])
            for item in items["AllHashTags"]:
                newHashTags.append(item)
        file.close()


    newHashTags = set(newHashTags)
    #pprint(newHashTags)

    FileName =  "HashTags.json"

    with open(os.getcwd() +  "/" + FileName , mode = 'r' , encoding="utf-8") as file:
        json_array = json.load(file)
        for item in json_array["HashTags"]:
            oldHashTags.append(item)

    

    # 資料夾與檔案是否存在
    if os.path.isfile(os.getcwd() +  "/" + FileName):
        file =open(os.getcwd() +  "/" + FileName , mode = 'w' , encoding="utf-8")
        print("檔案存在。")
    else:
        if not os.path.isdir(os.getcwd() ):
            os.mkdir(category)
        file = open(os.getcwd() +"/" + FileName , mode = 'w' , encoding="utf-8")
        print("檔案不存在，已創立" + FileName  )

    
    oldHashTags.extend(newHashTags)
    oldHashTags = set(oldHashTags)
    oldHashTags = sorted(list(oldHashTags))
    
    data = {"HashTags" : oldHashTags }
    # 寫入json檔並調整格式
    file.write(json.dumps( data ,ensure_ascii=False , indent=4, separators=(',', ': ')))
    file.close()
    #    if not os.path.isdir(os.getcwd() + "/"+ category + "/" + dir):
    #        os.mkdir(os.getcwd() + "/"+ category + "/" + dir)
    #    shutil.move(os.getcwd() + "/"+ category+ "/" + fileName , os.getcwd() + "/"+ category + "/" +dir )
    #print("insert DB done")


WriteAllHashTagsToMongoDB()