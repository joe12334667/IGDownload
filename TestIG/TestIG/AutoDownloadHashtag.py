import DownloadHashtagMutiThread
import time 
while True :
    tStart = time.time()
    category = ["食" , "衣" , "住" , "行" ]
    for cate in category:
        DownloadHashtagMutiThread.MutiTheadDownload(cate ,100)
        print(cate , " finish")
    

    tEnd = time.time()
    print("final time : %f s" % (tEnd - tStart))
    time.sleep(3600)