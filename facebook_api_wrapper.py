import facebook
import json
import urlparse

TEMP_DEFAULT_ACCESS_TOKEN_HERE = 'YOUR_ACCESS_TOKEN_HERE'
DEFAULT_PAGE_ID = 'nytimes'
DEFAULT_FIELDS = 'id,message,link,name,caption,description'
DEFAULT_MAX_POSTS = 90
QUERY_LIMIT_SIZE = 25


# A class that wraps all interaction with the Facebook API
class FacebookAPIWrapper(object):

    @classmethod
    def get_posts(cls, access_token=TEMP_DEFAULT_ACCESS_TOKEN_HERE,
                  object_id=DEFAULT_PAGE_ID, max_posts=DEFAULT_MAX_POSTS, fields=DEFAULT_FIELDS):
        '''
        Gets posts from the facebook api
        :param access_token: access token on which there is access to the posts and page
        :param object_id: the object id for example nytimes
        :param max_posts: maximum number of posts to fetch
        :param fields: which fields to get
        :return: returns a list of dictionaries on which each dictionary represents a post
        '''
        posts = []
        graph = facebook.GraphAPI(access_token=access_token, version='2.7')

        retrived_posts_counter = 0
        current_paging_token = None
        current_until = None
        limit = min(QUERY_LIMIT_SIZE, max_posts)

        while retrived_posts_counter < max_posts:

            try:
                feed = graph.get_connections(id=object_id, connection_name='feed', fields=fields,
                                             until=current_until,__paging_token=current_paging_token, limit=limit)

            except Exception as err:

                print "There was a problem accessing facebook API: %s" % err
                return []

            paging = feed.get('paging',None)

            if paging:

                # Documentation regarding until and __paging_token
                # https://jira.spring.io/browse/SOCIALFB-168
                current_until = urlparse.parse_qs(paging['next']).get('until',None)
                current_paging_token = urlparse.parse_qs(paging['next']).get('__paging_token',None)

            for post in feed.get("data",[]):
                retrived_posts_counter +=1
                posts.append(post)

            limit = min(QUERY_LIMIT_SIZE, (max_posts - retrived_posts_counter))

        return posts