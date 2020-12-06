from google.cloud import language_v1
from google.cloud.language_v1 import enums
import os
import langid
import pymysql.cursors

def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    return {"score" ,  "magnitude"}
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= os.getcwd() + "/GCPKey2.json"
    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages

    document = {"content": text_content, "type": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # Get overall sentiment of the input document
    #print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    #print(
    #    u"Document sentiment magnitude: {}".format(
    #        response.document_sentiment.magnitude
    #    ))

    return {"score" : response.document_sentiment.score , "magnitude" : response.document_sentiment.magnitude}
    # Get sentiment for all sentences in the document
    #for sentence in response.sentences:
    #    print(u"Sentence text: {}".format(sentence.text.content))
    #    print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
    #    print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))
    #    print("==========================================================================")
    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    #print(u"Language of the text: {}".format(response.language))



#text = """
#藝人小鬼（黃鴻升）本月16日在位於台北市北投區的住所驟逝，享年36歲。檢警相驗遺體後，初步排除外力介入，經家屬同意，檢警今天下午2時30分會同法醫在板橋殯儀館解剖釐清死因，結束後檢察官王乙軒步出解剖中心接受訪問，她指出，初步解剖發現，小鬼死因疑似是心血管的問題。

#小鬼在16日上午11時許被59歲父親發現時已無生命跡象，身上僅穿著白色短t、下身赤裸，他臉朝下趴地，口鼻流血、嘴唇撞腫，研判是慌張走出浴室，突然因不明原因摔倒，臉部撞到流血，屋內無發現藥物、也沒有喝酒情事。

#今天下午檢警會同法醫在板橋殯儀館進行解剖程序，小鬼父親與妹妹均到場，程序結束後，負責解剖程序的檢察官王乙軒接受訪問，表示初步解剖發現，小鬼死因疑似是心血管的問題，沒有明顯外傷，遺體已經發還家屬，詳細死因還有待法醫研究所的鑑定報告。

#小鬼驟逝的消息傳出，引發娛樂圈一片不捨，許多藝人紛紛在社群軟體上發表哀弔文，他的靈堂設置在龍巖A館301室，於19日至21日開放3天，每天上午10點至傍晚6時，僅開放親友弔唁，並懇辭奠儀與花籃。
#"""
#ans = sample_analyze_sentiment(text)


print("connect...") 
connection = pymysql.connect("140.131.114.143","root","superman12334667","instabuilder" ,  charset='utf8mb4' )
print("connect success")
with connection.cursor() as cursor:
    sql = "SELECT * FROM instabuilder.comment where isnull(pn)"
    cursor.execute(sql)
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        #post_no, comment_account, content, comment_time, pn, pn_score
        print(row)
        ans = sample_analyze_sentiment(row[2])
        print(ans)
        print("\n ============================ \n")
        if ans["score"] > 0:
            sentiment = "positive"
        elif ans["score"] == 0:
            sentiment = "neutral"
        elif ans["score"] < 0:
            sentiment = "negative"

        sql = "update comment set pn = %s , pn_score = %s where post_no = %s and comment_account = %s and comment_time = %s;"
        cursor.execute(sql , (sentiment , ans["score"] , row[0] , row[1] , row[3] ))
        connection.commit()

connection = 0







