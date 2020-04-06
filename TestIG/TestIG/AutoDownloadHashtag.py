import DownloadHashtagMutiThread
import time 
import pprint

runtime = 0
category = ["食" , "衣" , "住" , "行" ]
finaltimes = {}
while True :
    runtime +=1
    tStart = time.time()
    for cate in category:
        DownloadHashtagMutiThread.MutiTheadDownload(cate ,100)
        print(cate , " finish")
    

    tEnd = time.time()
    finaltime = tEnd - tStart
    finaltimes[runtime] = finaltime
    print("runtime :" ,runtime , "final time : %f s" % finaltime )
    print("final time : ")
    pprint.pprint(finaltimes)
    time.sleep(3600)