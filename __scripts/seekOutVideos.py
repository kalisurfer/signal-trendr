import twitter
import re
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit
tweetCollection = db.tweet
gamesCollection = db.games
historyCollection = db.game_history
ytVids = db.video

config = [
	]

# run through games and figure out matches to tweets whose gameID = 0


#results = tweetCollection.find({"$and": [{ "text" : {"$regex" : "final fantasy"}}, {"game": 0}]});
#results = tweetCollection.find({"$and": [{ "text" : re.compile("final fantasy", re.IGNORECASE)}, {"game": 0}]});
#if (results.count() > 0):
#	print("there was at least one match for ", results.count())
#	for d in results:
#		print("***********************")
#		print(d.get("text"))
#		print(d.get("author"))
#		print("***********************")
	

#	print("no matches for")

def update_game(game_id, score):
	gamesCollection.update({"_id": ObjectId(game_id)}, {"$inc": {"trendIndex": score}})

gamesSearch = gamesCollection.find({});

for c in gamesSearch:
	for tag in c.get("tags", []):
		print("seeking matches for ", tag)
		results = ytVids.find({ "title" : re.compile(tag, re.IGNORECASE) });  
		if (results.count() > 0):
			print("there was", results.count(), " match for ", tag)
			for d in results:

				print("***********************")
				print(d.get("title"))
				print(d.get("author"))
				print("***********************")

			#	tweetCollection.update({"_id": d.get("_id")}, {"$set": {"game": c.get("id")}})
			#	update_game(c.get("id"), d.get("score"))
			#	print("updated DB")
			
		else:
			print("no matches for ", c.get("name"), "and the tag ", tag)





