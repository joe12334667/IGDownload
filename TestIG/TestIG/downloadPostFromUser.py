# -*- coding: utf-8 -*-
from instaloader import Instaloader, Profile 
import pymysql.cursors
import time
import datetime

connection = pymysql.connect("140.131.115.97","root","12334667","instabuilder" ,  charset='utf8mb4' )
i = 0
l = Instaloader(quiet=True, compress_json=False , max_connection_attempts = 10)
profile = Profile.from_username(l.context , "joe_try_something")
for post in profile.get_posts():
    i+=1
    if i>= 10 : break
    print("mediaid :" , post.mediaid)
    print("caption :" , post.caption)
    print("likes :" , post.likes )
    print("pcaption :" , post.pcaption)
    print("caption_hashtags :" , post.caption_hashtags)
    #案讚的帳號
    for like in post.get_likes():
        print("get_likes :" , like )
    for comment in post.get_comments():
        print("comments :")
        print(comment.owner.username  , " : " , comment.text)
    insta_post_id = post.mediaid
    try:
        #with connection.cursor() as cursor:
        #    # Create a new record
        #    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        #    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        ## connection is not auto commit by default. So you must commit to save
        ## your changes.
        #connection.commit()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM instabuilder.post where insta_post_id = %s"
            cursor.execute(sql , (insta_post_id))

            #為空值，找不到這筆紀錄
            if(not  cursor.fetchall()):
                print("新增一筆POST")
                sql = "insert into post (insta_post_id, content , announcer_no , announce_time ) value (%s , %s , %s , %s)"
                cursor.execute(sql, (insta_post_id , post.caption , 3 , datetime.datetime.now() ))
                connection.commit()

                sql = "SELECT post_no FROM instabuilder.post where insta_post_id = %s;"
                cursor.execute(sql , (insta_post_id))
                connection.commit()
                #有沒有新增到資料庫
                data = cursor.fetchall()
                if( not data):

                    print("新增失敗 insta_post_id :" , insta_post_id)

                else :

                    print("成功新增 insta_post_id :" , insta_post_id)
            
            sql = "SELECT post_no FROM instabuilder.post where insta_post_id = %s;"
            cursor.execute(sql , (insta_post_id))
            
            data = cursor.fetchone()
            print("data :" , data[0])
            
            



            post_no = data[0]
            print("post_no :" ,post_no)

            print("新增 like record")
            print("person who like this post :")
            for likes_profile in post.get_likes():
                print( likes_profile.username ,end = " , ")

                #確認有沒有新增過
                sql = "SELECT post_no FROM instabuilder.like where post_no = %s and like_account = %s;"
                cursor.execute(sql, (post_no , likes_profile.username))
                like_data = cursor.fetchall()
                if( not like_data):
                    #資料庫無此like
                    sql = "insert into instabuilder.like ( post_no, like_account , like_time) value ( %s , %s , %s);"
                    cursor.execute(sql, (post_no ,likes_profile.username , datetime.datetime.now() ))
                    connection.commit()
                        

            print("新增 comment record")
            print("person who comment this post :" )
            for comment in post.get_comments():
                print( comment.owner.username  , "comment text : ", comment.text , end = " , ")
                        
                #確認有沒有新增過
                sql = "SELECT post_no FROM instabuilder.comment where post_no = %s and comment_account = %s;"
                cursor.execute(sql, (post_no , comment.owner.username))
                comment_data = cursor.fetchall()
                if( not comment_data):
                    #資料庫無此comment
                    sql = "insert into comment (post_no, comment_account, content ,  comment_time) value (%s , %s , %s , %s)"
                    cursor.execute(sql, (post_no ,comment.owner.username , comment.text , comment.created_at_utc + datetime.timedelta(hours=8) ))
                    connection.commit()

                    
            print("新增hashtags")
            print("hashtag which in caption without # ")
            for hashtag in post.caption_hashtags:
                print(hashtag , end = " , ")
                        
                #確認有沒有新增過在hashtagCates
                sql = "SELECT hashtag_no FROM instabuilder.hashtagCates where hashtag = %s ;"
                cursor.execute(sql, (hashtag))
                hashtag_data = cursor.fetchall()
                if( not hashtag_data):
                    #資料庫無此HASHTAG
                    sql = "insert into hashtagCates (hashtag , stage ) value (%s , %s);"
                    cursor.execute(sql, (hashtag , 0))
                    connection.commit()

                #獲取hashtag_no 來 insert to hashpost
                sql = "SELECT hashtag_no FROM instabuilder.hashtagCates where hashtag = %s ;"
                cursor.execute(sql, (hashtag))
                hashtag_data = cursor.fetchall()
                hashtag_no = hashtag_data[0]
                        
                #確認有沒有新增過
                sql = "SELECT no FROM instabuilder.hashpost where post_no = %s and hashtag_no = %s ;"
                cursor.execute(sql, (post_no , hashtag_no))
                hashtag_data = cursor.fetchall()
                if( not hashtag_data):
                    #資料庫無此HASHTAG    
                    sql = "insert into instabuilder.hashpost (post_no, hashtag_no) value  (%s,%s);"
                    cursor.execute(sql, ( post_no , hashtag_no))
                    connection.commit()
    finally:
        #connection.close()
        print("finally")





















