# this file will help create some of the basic framework needed to fill out the site

#import tweetstream
import datetime
import json
import re
import string
from bson.objectid import ObjectId
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

start = datetime.datetime(2015, 01, 01, 9, 0, 0, 0)

# game scaffolding
gameCollection = db.games
videoCollection = db.video
tweetCollection = db.tweet
historyCollection = db.game_history


#gamesWithoutYT = gameCollection.find({"recent_rank": {"$gt": 0}, "ytChannel": None})
#gamesWithoutYT = gameCollection.find({"ytChannel": None})

#tweets = tweetCollection.remove({"created_at": {"$lt": start}})
print "tweets.count()"

#deleteVideo = videoCollection.remove({"game": ObjectId("528b1afee4b0b33de7a6c44b") })

#print deleteVideo.count()

'''
for game in gamesWithoutYT:
	videos = videoCollection.find({"game": game.get('_id')})
	#videoCollection.remove({"game": game.get('_id')})
	if videos.count() >= 0:
		print "____________________________________________"
		print videos.count()
		print game.get('_id')
		print game.get('title')
		#videos = videoCollection.find({"game": game.get('_id')})
		print "____________________________________________"



listing = gameCollection.find({});



for listings in listing:
    listing_id = listings.get('_id')
    print listings.get('trailer')
    trailers = listings.get('trailer', [])
    if isinstance(trailers, basestring):
        trailers = [trailers]
    if len(trailers):
        trailer = trailers[0]
        print listing_id, trailer.split("/")[-1]
        print "----------------------------------------"
    else:
        print listing_id, "has none"
        print "----------------------------------------"



tags = set()

for game in games:
	genre = game.get("genre", [])
	if isinstance(genre, basestring):
		genre = [genre]
	for tag in genre:
		tags.add(tag)


for tag in tags:
	print tag




#tweets = tweetCollection.remove({"game": 0, "created_at": {"$lt": start}})


#tweets = tweetCollection.find({"game": 0, "created_at": {"$lt": start}})

ranks = historyCollection.find({"dateAdded": {"$gte": start}}).sort("rank", -1)
print ranks.count()
for rank in ranks:
	print rank.get('rank')
	print rank.get('dateAdded')
	print "----------------"

'''

#results = tweetCollection.find({"$and": [{ "text" : re.compile("duet", re.IGNORECASE)}, {"tweettype": 3} ,{"game": ObjectId("5266244de4b0a5a46e8e9cde")}]}); 
'''
results = tweetCollection.remove({"game": ObjectId("523805a5e4b08583f464bc34"), "tweettype": 3})
tweetCollection.update( 
		{{"text" : re.compile("racing game", re.IGNORECASE)}, {"game": ObjectId("523805a5e4b08583f464bc34")}}, 
		{"$set" : {"game" : 1} }
		) 


print results.count()
for result in results:
	print result.get('text')
	print "---------"
'''	#tweetCollection.remove({"_id": result.get('_id')})
'''	tweetCollection.update(
		{"_id": result.get('_id')},
		{"$set": {"game": 1}}
);

tweetCollection.update(
	{"game": 1},
	{"$set": {"game": ObjectId('5266244de4b0a5a46e8e9cde')}}
);


'''



	

'''
for game in listing:
	trailers = [json.JSONDecoder(game.get('trailer'))];
	#trailers = game.get('trailer');
	print("---------------------")
	print(game.get('_id'), ' for ', game.get('title'), '+ description = ', game.get('description'));
	print len(trailers);
	print trailers[0]

	#gameCollection.update(
	#	{"_id": ObjectId(game.get('_id'))}, 
	#	{"$set": {"description": "No description yet"}}
	#	);
'''

#http://cdn.superbwallpapers.com/wallpapers/games/call-of-duty-ghosts-19880-400x250.jpg

# set of arrays to get games in
# {"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "tags": ["assassin's creed black flag", "acblackflag"]}
#gameCollection.update({}, { "$set": {"trendIndex": 0}}, upsert=False, multi=True)

#results = gameCollection.find({"releaseDate": { "$gt": datetime.datetime.utcnow() }});
#results = gameCollection.find({ "heroURL" : {"$not":{"$regex" : ".*localhost.*"}}});

#results = gameCollection.find({ "heroURL" : {"$regex" : ".*lorempixel.*"}});
#for result in results:
#	newDateArray = [] 
#	#newDateArray = string.split(result.get('releaseDate'), "-");
#	print result.get('title')
#	print result.get('_id')
#	print result.get('heroURL')
	#print newDateArray[0]
	#newDate = datetime.datetime.date(newDateArray[1], newDateArray[2], newDateArray[0])
	#newDate = datetime.datetime(2013, 5, 1, 12, 00, 00)
#	gameCollection.update( 
#		{"_id": result.get('_id')}, 
#		{"$set" : {"heroURL" : "http://placehold.it/980x647&text=HeroArt"} }
#		)



	#print "the new date is "
	#print newDate
	#print "****** /n"