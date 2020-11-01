# -*- coding: utf-8 -*-
from instaloader import Instaloader, Profile 
import pymysql.cursors
import time
import datetime
from datetime import timedelta  

def downloadUserFollowers(user):
    print("connect...") 
    #connection = pymysql.connect("140.131.114.143","root","superman12334667","instabuilder" ,  charset='utf8mb4' )
    connection = pymysql.connect("instabuilderdb.cmjbghjyygh8.ap-northeast-1.rds.amazonaws.com","root","superman12334667","instabuilder" ,  charset='utf8mb4' )
    print("connect success")

    l = Instaloader(quiet=False, compress_json=False , max_connection_attempts = 10)
    profile = Profile.from_username(l.context , user)
    l.login("joe_try_something"  , "joe12334667")  
    
    cursor = connection.cursor()

    allfollowers = profile.get_followers()
    allfollowers_id = list();
    add_followers = 0
    delete_followers = 0

    #$新增新追蹤者
    for follower in allfollowers :
        allfollowers_id.append(follower.userid)
        sql = "SELECT * FROM instabuilder.followers where id = %s and account_id = (select account_id from instaaccount where account_name = %s);"
        cursor.execute(sql , ( follower.userid , user))
        connection.commit()
        records = cursor.fetchall()
        print("follower.username :",follower.username)
        if (records):
            print("already have")
            continue 
        else:
            add_followers += 1
            sql = "insert into followers (id, account_id, name, follow_date) value (%s ,(select account_id from instaaccount where account_name = %s) , %s ,now());"
            cursor.execute(sql , ( follower.userid , user , follower.username))
            connection.commit()
    
    #取得資料庫所有的追蹤者ID
    sql = "SELECT id FROM instabuilder.followers where account_id = (select account_id from instaaccount where account_name = %s);"
    cursor.execute(sql , ( user))
    connection.commit()
    records = cursor.fetchall()
    if (not records):
        print("not follower in DB")
    else:
        #如果退追，則刪除資料
        for record in records:
            id = int(record[0])
            if id not in allfollowers_id:
                delete_followers += 1
                print("delete " , id , " user" )
                sql = "delete from followers where id = %s and account_id = (select account_id from instaaccount where account_name = %s);"
                cursor.execute(sql , ( id ,user))
                connection.commit()
    print("add_followers :" , add_followers)
    print("delete_followers :" , delete_followers)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
downloadUserFollowers("13_23_33_")