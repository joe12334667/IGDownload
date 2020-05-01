from instaloader import Instaloader, Profile , Hashtag

    
L = Instaloader()
hashtag = Hashtag.from_name(L.context, "北商")
L.save_structure_to_file(hashtag , "北商")
#print("name:" ,hashtag.name  )
#print("hashtagid:" ,hashtag.hashtagid  )
#print("profile_pic_url:" ,hashtag.profile_pic_url  )
#print("description:" ,hashtag.description  )
#print("allow_following:" ,hashtag.allow_following  )
#print("is_following:" ,hashtag.is_following  )
#print("is_top_media_only:" ,hashtag.is_top_media_only  )
#print("allow_following:" ,hashtag.allow_following  )
#print("allow_following:" ,hashtag.allow_following  )


