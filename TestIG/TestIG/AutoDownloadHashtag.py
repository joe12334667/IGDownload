import DownloadHashtagMutiThread
import testMongoDb
import time 
import pprint


runtime = 0
#category = ["食" , "衣" , "住" , "行" ]
finaltimes = {}
while True :
    #runtime +=1
    #tStart = time.time()
    #for cate in category:
    #    DownloadHashtagMutiThread.MutiTheadDownloadByCategory(cate ,100)
    #    print(cate , " finish")
    try :    
        DownloadHashtagMutiThread.DownloadAllHashTags(100)
    except:
        print("-"*30)
        print("except")
        print("-"*30)
    #tend = time.time()
    #finaltime = tend - tstart
    #finaltimes[runtime] = finaltime
    #print("runtime :" ,runtime , "final time : %f s" % finaltime )
    #print("final time : ")
    #pprint.pprint(finaltimes)
    
    #testMongoDB.WriteAllHashTagsToMongoDB()
    #time.sleep(3600)
