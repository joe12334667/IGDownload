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
    i = 0
    l = Instaloader(quiet=True, compress_json=False , max_connection_attempts = 10)
    profile = Profile.from_username(l.context , user)
    l.login("joe_try_something"  , "joe12334667")  
    
    cursor = connection.cursor()
    for follower in profile.get_followers() :
        sql = "insert into followers (id, account_id, name, follow_date) value (%s ,(select account_id from instaaccount where account_name = %s) , %s ,now());"
        cursor.execute(sql , ( follower.userid , user , profile.username))
        connection.commit()


downloadUserFollowers("13_23_33_")