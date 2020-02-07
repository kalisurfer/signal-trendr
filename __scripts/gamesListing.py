# this file will help create some of the basic framework needed to fill out the site

import tweetstream
import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

# game scaffolding
gameCollection = db.games
listing = gameCollection.find({});

# set of arrays to get games in
# {"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "tags": ["assassin's creed black flag", "acblackflag"]}
for i in listing:
	print "{id:}",i["_id"],"name",i["title"]
	#print "\n"
	#print "-----" * 5
