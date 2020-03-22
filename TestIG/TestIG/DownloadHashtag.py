from datetime import datetime
from itertools import dropwhile, takewhile
import time

import instaloader

tStart = time.time()
HashTag = "泥泥汝流水帳"
L = instaloader.Instaloader(quiet = False , compress_json=False )
AllHashTags = list()
posts = L.get_hashtag_posts(HashTag)
# or
# posts = instaloader.Profile.from_username(L.context, PROFILE).get_posts()

L.download_hashtag(HashTag , max_count = 30 )

#SINCE = datetime(2020, 2, 10)
#UNTIL = datetime(2020, 2, 17)
#print(posts)
#i = 0
#for post in posts :
    
#    if post.date > SINCE and post.date < UNTIL :
        
#        if not post.caption_hashtags :
#        因為當字符串或集合為空時，其值被隱式地賦為False。
#            print ("pass")
#            print("hashtags : " , post.caption_hashtags)
#            continue
#        i+=1
#        print(i , "\nusername : " , post.owner_username)
#        print("likes : ",post.likes )
#        print("hashtags : " , post.caption_hashtags)
        

#        AllHashTags.extend(post.caption_hashtags)

#        L.download_post(post , "#" + HashTag)
#    if i == 100:
#        print(i , " break")
#        break

tEnd = time.time()
#AllHashTags = set(AllHashTags)
#print("All HashTags : " ,  AllHashTags  )
print("time : %f s" % (tEnd - tStart))



#for post in takewhile(lambda p: p.date > until, dropwhile(lambda p: p.date > since, posts)):
#    print(post.date)
#    l.download_post(post, '#urbanphotography')