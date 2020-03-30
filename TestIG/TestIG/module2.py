import re
ret_search = re.search("^[\u4e00-\u9fa5_a-zA-Z0-9]+$","陳joe123") #掃描整個字串返回第一個匹配到的元素並結束，匹配不到返回None
if(ret_search):
    print("yes")
else:
    print("not")