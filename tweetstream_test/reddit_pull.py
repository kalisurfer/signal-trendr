#methodology of pulling reddit posts.

#grab top 10 posts from subreddit X, then grab comments from those.

#syntax: sumbmissions = r.get_subreddit('python').get_top(limit=X)
#        submission = submissions.next()
#        submission.comments <---now a list of all comments.

#remember to identify your user agent more than just default python/urllib2

#requests.get('http://httpbin.org/headers', hooks=hooks, headers=headers)
#{
#    "headers": {
#        "Content-Length": "",
#        "Accept-Encoding": "gzip",
#        "Yo": "dawg",
#        "X-Forwarded-For": "::ffff:24.127.96.129",
#        "Connection": "close",
#        "User-Agent": "python-requests.org",
#        "Host": "httpbin.org",
#        "X-Testing": "True",
#        "X-Forwarded-Protocol": "",
#        "Content-Type": ""
#    }
#}

#import reddit

"""headers contain the headers to be sent along with the request"""
headers = {'User-Agent':'Python/VideoGameOpinionScraper'}

"""auth contains any required login information"""
auth = {'user':'pass'}

#r = reddit.Reddit(user_agent = 'HopefullyNonintrusiveGameCommentScraper')

