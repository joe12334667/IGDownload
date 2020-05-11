from instaloader import Instaloader, Profile 
import pymysql.cursors
import time

connection = pymysql.connect("140.131.115.97","root","12334667","instabuilder" )
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
    #案讚的帳號
    for like in post.get_likes():
        print("get_likes :" , like )

    postid = post.mediaid
    try:
        #with connection.cursor() as cursor:
        #    # Create a new record
        #    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        #    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        ## connection is not auto commit by default. So you must commit to save
        ## your changes.
        #connection.commit()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM instabuilder.post where post_id = %s;"
            cursor.execute(sql , (postid))
            #為空值，找不到這筆紀錄
            if(not  cursor.fetchall()):
                print("新增一筆POST")
                sql = "insert into 'post' ( 'post_id' , 'content' ) value (%s , %s)"
                cursor.execute(sql, (postid , post.pcaption ))

                sql = "SELECT 'post_no' FROM instabuilder.post where post_id = %s;"
                cursor.execute(sql , (postid))

                #有沒有新增到資料庫
                data = cursor.fetchall()
                if( not data):

                    print("新增失敗 post id :" , postid)

                else :

                    print("成功新增 post id :" , postid)
                    print("新增 like record")
                    post_no = data[0]
                    for likes_profile in post.get_likes():
                        print("person who like this post :" , likes_profile.username ,end = " , ")
                        sql = "INSERT INTO 'like' ( 'post_no','like_account' , 'like_time') value ( %s,%s,%s)"
                        cursor.execute(sql, (post_no ,likes_profile.username , time.time() ))

                    for comment in post.get_comments():
                        print("person who comment this post :" , comment.owner.username  , "comment text : ", comment.text , end = " , ")
                        
                        sql = "insert into 'comment' (post_no, comment_account, comment_time) value (%s , %s ,%s)"
                        cursor.execute(sql, (post_no ,comment.owner.username , comment.created_at_utc ))

                        



    finally:
        connection.close()





















