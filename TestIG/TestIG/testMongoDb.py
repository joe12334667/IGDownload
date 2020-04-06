import pymongo
import json
import os
import time
import shutil 
from os import listdir
from pprint import pprint

def WriteHashTagsToMongoDB(category):


    categorylist = {"食" : "Food" , "衣" : "Clothes" , "住" :"Live" , "行" :"Travel" }
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



category = ["食" , "衣" , "住" , "行" ]
for cate in category:
    WriteHashTagsToMongoDB(cate)




