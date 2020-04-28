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

HashTags = "joe12334667"
HashTag = "#"+ HashTags
# Get instance
L = Instaloader(quiet=False, compress_json=False )

AllHashTags = list()
    
countRunTime = 0
try :
    print("cbg")
    posts = L.get_hashtag_posts(HashTags)
    print("abc")
    #print(1.55/0)
    for post in posts :
        print("234")
        #沒有hashtags
        #因為當字符串或集合為空時，其值被隱式地賦為False。
        if not post.caption_hashtags :
                continue

        countRunTime +=1
        #確認是否新增進HashTags
        for item in post.caption_hashtags:
            #if is_all_chinese_And_English(item):
                AllHashTags.append(item)
        #統計多少篇
        if countRunTime == RunTime :
            break
except Exception  as e:
    print("123")
    print(e)