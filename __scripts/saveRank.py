# this goes through the games in the DB and updates their rank in the history building table
# Game ID - unique ID
# Date - Date
# Rank - what place was this game
# Value - perhaps an absolute value of popularity? Something you can use to find out if #1 on 8/1 was more popular in absolute terms to #1 on 12/15

import twitter
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit
tweetCollection = db.tweet
gamesCollection = db.games
gameHistory = db.game_history
i = 0;
#ts = time.time()
#isodate = datetime.datetime.fromtimestamp(ts, None)
#get all games sorted by trendIndex


nowStamp = datetime.now()
#newDate = datetime.datetime.date(2013, 5, 1, 12, 00, 00)

def dateToISOString(dateObject):
	return dateObject.strftime("%Y%m%dT%H%M%S")



results = gamesCollection.find({}).sort("trendIndex", -1)

for games in results:
	i = i + 1

	post = {
		"game": games.get("_id"),
		"trendIndex": games.get("trendIndex"),
		#"dateAdded": dateToISOString(nowStamp),
		"dateAdded": nowStamp,
		"rank": i
	}
	gameHistory.save(post)
	print "************"
	#print games.get("title")
	print("trendIndex is ", games.get("trendIndex"))
	print("in ", i, " position")
	print("date is ", nowStamp)
