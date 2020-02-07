from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit
tweetCollection = db.tweet

limit = datetime.utcnow() - timedelta(days=7)

talkingAbout = tweetCollection.find({"game": 0, "created_at": {"$gte": limit}}).sort("created_at", -1)

if (talkingAbout.count() > 0):
	print("WE GOT RESULTS.  LIKE ", talkingAbout.count(), " OF THEM")
	for tweets in talkingAbout:
		# to feed csv
		print( tweets.get("author") , ",", tweets.get("text"))
		#print tweets.get('created_at')

		#print "*******************************"
		#print("BY ", tweets.get("author"), " SCORED ", tweets.get("score"))
		#print " "
		#print tweets.get("text")
		#print tweets.get("created_at")
		#print tweets.get("_id")
		#print " "
		#print "*******************************"
else:
	print "NO RESULTS"
