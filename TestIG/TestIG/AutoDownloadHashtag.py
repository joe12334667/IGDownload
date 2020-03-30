import DownloadHashtagMutiThread
import time 

tStart = time.time()
category = ["食" , "衣" , "住" , "行" ]
for cate in category:
    DownloadHashtagMutiThread.MutiTheadDownload(cate ,10)
    print(cate , " finish")
    time.sleep(5)

tEnd = time.time()
print("final time : %f s" % (tEnd - tStart))