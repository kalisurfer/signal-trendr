# this file will help create some of the basic framework needed to fill out the site

import tweetstream
import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

# game scaffolding
gameCollection = db.games
listing = gameCollection.find();

# set of arrays to get games in
# {"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "tags": ["assassin's creed black flag", "acblackflag"]}
for i in listing:
	do_update = False
	update = {}
	if i.get("heroURL", "")[:16] == "http://localhost":
		update["heroURL"] = i.get("heroURL", "")[21:]
		do_update = True
	if i.get("thumbUrl", "")[:16] == "http://localhost":
		update["thumbUrl"] = i.get("thumbUrl", "")[21:]
		do_update = True
	if do_update:
		print "updating {0}".format(i["_id"])
		gameCollection.update({"_id": i["_id"]}, {"$set": update})

