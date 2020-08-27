import re
import zhon
from zhon import hanzi
import string
def Change_to_all_chinese_And_English(strs):
    ans = ""
    for _char in strs:
        if _char in hanzi.punctuation or _char in string.punctuation or _char == " ":
            ans += _char
            continue
        ret_search = re.search("^[\u4e00-\u9fa5_a-zA-Z0-9]+$",_char) 
        if(ret_search):
            ans += _char
    
    return ans


#print(Change_to_all_chinese_And_English("""
#嘉義市范姓老翁昨晚近8時帶疑似鹽酸液體，到張姓妻子住的長期照護中心，先拿酸液灌妻子，再以床單悶住妻口鼻，范也自飲鹽酸送醫急救不治，妻子搶救後狀況穩定。據悉，范翁每天都會來照護中心照顧，但妻子長期臥床插鼻胃管，已成「半植物人」狀態，疑似不忍妻子長期痛苦才會下手，范的親友也感嘆「夫妻倆感情很好，怎會發生此事..」

#范姓夫妻育有4名兒女，中心人員也常可見兒女來照顧，i am Handsome，最近都未發現父親有異常，市府社會處指出，范家非低收入、中低收入戶或邊緣戶，但入住照護中心有申請身心障礙者補助，已派遣社工了解。
#"""))


text = "🎊仁美學區高樓視野三房平車買屋再送20坪露臺🎊\n🌲晴山居視野三房平車買屋再送20坪露臺🌲🌲\n🏨台中市北屯區四平路238巷388號\n🏨建坪52.09坪\n🏨室內坪數29.34坪+20坪露臺使用坪約49坪\n🏨高樓永久視野戶採光通風佳\n🏨屋齡1年\n🚙B1平面車位好停車\n🌲多功能露臺空中花園休憩使用區\n✨✨🎉🎉售價1468萬🎉🎉✨✨ ☀☀三面採光1共用壁永久視野☀☀\n✨✨溫暖幸福房子✨✨\n🌲環境優美🚲 雙商圈🚶‍♂️ 九年國教免接送👨‍👩‍👦\n讓您在下班回家後享受悠活的居住環境\n🌲雙商圈精華地段\n🚙生活機能機能交通便利\n🍱市場百貨小吃林立\n🎊🎊社區質感佳定期保養管理嚴謹🎊🎊 📱歡迎來電預約看屋咨詢☎️097060804金家行☎️\n📱LINE ID:peter28(搜尋手機號碼即可) ------------------------------------------------------------------\n💎六家團隊上千物件百人銷售成交最快\n💎住商不動產北屯823公園店歡迎委託\n💎已銷售西區北區北屯11期周遭知名建設品牌\n💎我一定會站在您的立場全力以赴去爭取\n💎若您有任何不動產相關買賣問題\n💎可立即幫您代尋您要的房子及需求\n💎請您不吝來電 📱歡迎來電咨詢☎️097060804金家行☎️\n📱LINE ID:peter28(搜尋手機號碼即可)\n------------------------------------------------------------------\n🔥住商不動產北屯823公園店\n🔥專賣各區新大樓豪宅大樓別墅產品\n🔥鑽石般的團隊誠徵\n🔥具強烈企圖心、熱情、不滿於現況想改變\n🔥想更突破渴望年薪千萬的經紀人及社會新鮮人\n🔥我們給予您最完善的教育制度及福利\n🔥提供最強大的資源\n🔥只要您企圖心跟執行力夠強\n🔥千萬年薪不是夢\n📱歡迎來電預約面試☎️04-24222788☎️ 豪宅#823紀念公園#台中#Taichung#台中11期#室內設計#台中重劃區#四張犁#四張犁公園#北屯區#住宅#居家#不動產#房地產#崇德商圈#洲際棒球場#八二三紀念公園#住商不動產#仁美國小#台中11期重劃區#11期重劃區#Beitundist#住商不動產北屯823公園店#台中14期#台中14期重劃區#morrisonacademy#realestate#realty"
text = text.replace("#" , "")
text = text.replace("realty" , "")
text = text.strip()
text = Change_to_all_chinese_And_English(text)
print(text)
#print(re.search("^[\u4e00-\u9fa5_a-zA-Z0-9]+$" , """
#嘉義市范姓老翁昨晚近8時帶疑似鹽酸液體，到張姓妻子住的長期照護中心，先拿酸液灌妻子，再以床單悶住妻口鼻，范也自飲鹽酸送醫急救不治，妻子搶救後狀況穩定。據悉，范翁每天都會來照護中心照顧，但妻子長期臥床插鼻胃管，已成「半植物人」狀態，疑似不忍妻子長期痛苦才會下手，范的親友也感嘆「夫妻倆感情很好，怎會發生此事..」

#范姓夫妻育有4名兒女，中心人員也常可見兒女來照顧，最近都未發現父親有異常，市府社會處指出，范家非低收入、中低收入戶或邊緣戶，但入住照護中心有申請身心障礙者補助，已派遣社工了解。
#"""))
#print(hanzi.punctuation)
#print(string.punctuation)