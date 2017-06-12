import json
from facebook_api_wrapper import FacebookAPIWrapper

SAVE_TO_FILE = True

posts = FacebookAPIWrapper.get_posts()
print "Total Posts: %s" % len(posts)

if SAVE_TO_FILE:

    file = open('posts.txt', 'w')
    file.write(json.dumps(posts))
    file.close()
else:

    print json.dumps(posts)