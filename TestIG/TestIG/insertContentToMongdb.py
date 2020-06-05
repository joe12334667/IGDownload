import pymongo
import json
import os
import time
import shutil 
from os import listdir
from pprint import pprint
#--------------------------------------WriteCategoryHashTagsToMongoDB--------------------------------------------
def WriteCategoryHashTagsToMongoDB(category):

    #Switch
    categorylist = {"食" : "Food" , "衣" : "Clothes" , "住" :"Live" , "行" :"Travel" }

    #連接資料庫
    myclient = pymongo.MongoClient(host='localhost', port=27017)
    db = myclient["Hashtags"]
    collect = db[categorylist[category]]
    

    files = listdir(os.getcwd() + "/"+ category)
    #pprint(files)
    dir =  "MongoDB_" + time.strftime("%Y-%m-%d_%H-%M") + category

    for fileName in files:
        if os.path.isdir(os.getcwd() + "/"+ category + "/" +fileName):
            continue
        file =open(os.getcwd() + "/"+ category + "/" + fileName , mode = 'r' , encoding="utf-8")
        json_array = json.load(file)

        for items in json_array[category]:
            print(items["hashtags"])
            print(items["AllHashTags"])
            post_id = collect.insert_one(items).inserted_id
            print(post_id)

        file.close()
        if not os.path.isdir(os.getcwd() + "/"+ category + "/" + dir):
            os.mkdir(os.getcwd() + "/"+ category + "/" + dir)
        shutil.move(os.getcwd() + "/"+ category+ "/" + fileName , os.getcwd() + "/"+ category + "/" +dir )




#---------------------------------------WriteAllHashTagsToMongoDB------------------------------------------------------
def WriteAllHashTagsToMongoDB():

    print("insert DB")
    print("Please wait")
    category = "Captions"
    #連接資料庫
    myclient = pymongo.MongoClient(host='localhost', port=27017)
    #DataBase
    db = myclient["Captions"]
    #collection = sheet
    collect = db["AllCaptions"]
    
    #抓出資料夾所有的檔案
    files = listdir(os.getcwd() + "/"+ category)
    #pprint(files)
    dir =  "MongoDB_" + time.strftime("%Y-%m-%d_%H-%M") + category

    for fileName in files:
        #不要資料夾
        if os.path.isdir(os.getcwd() + "/"+ category + "/" +fileName):
            continue
        #開檔
        file =open(os.getcwd() + "/"+ category + "/" + fileName , mode = 'r' , encoding="utf-8")
        print('open ' , fileName)
        json_array = json.load(file)

        for items in json_array['HashTags']:
            #print(items["hashtags"] , end =" , ")
            #pprint(items["AllHashTags"])
            #寫入資料庫
            post_id = collect.insert_one(items).inserted_id
            #print(post_id)

        file.close()
        if not os.path.isdir(os.getcwd() + "/"+ category + "/" + dir):
            os.mkdir(os.getcwd() + "/"+ category + "/" + dir)
        shutil.move(os.getcwd() + "/"+ category+ "/" + fileName , os.getcwd() + "/"+ category + "/" +dir )
    print("insert DB done")



#category = ["食" , "衣" , "住" , "行" ]
#for cate in category:
#    WriteCategoryHashTagsToMongoDB(cate)
WriteAllHashTagsToMongoDB()





