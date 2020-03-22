import instaloader
from instaloader import Instaloader, Profile

# Get instance
L = instaloader.Instaloader(quiet=True, compress_json=False)

# Optionally, login or load session
L.login("joe_try_something", "joejoe12334667" )        # (login)
#L.interactive_login(USER)      # (ask password on terminal)
#L.load_session_from_file(USER) # (load session created w/
                               #  `instaloader -l USERNAME`)
profile = Profile.from_username(L.context, "joe_try_something")
i = 0
count_likes = 0
for post in profile.get_posts():
    i+=1
    print(i , ":" , post.likes)
    print("hashtags : " , post.caption_hashtags)
    count_likes+=post.likes
    L.download_post(post, target=profile.username)
    if i==10 :
       break

print("total ig likes : " , count_likes )