# this file will start grabbing tweets from the weareplaying list on twitter

import twitter
import pprint
import datetime
import string
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

# game scaffolding
tweetCollection = db.tweet
pp = pprint.PrettyPrinter(indent=4)



api = twitter.Api(
			consumer_key='BzfccKOYg0dqn05kFewHw',
			consumer_secret='y005oSkVM2k3CNN32GQxKk7YUJPOhA92Rj8Ij8tJnQ0',
			access_token_key='13264102-NMZFOKySbIqDwsPu5KVttcy2dNfmNb5uvyJu5GY',
			access_token_secret='tCLLpOsmbfzEpsjOkOnBlBKvMPJz1JPFc6DFBmknfTU')


#print "updating everything in the table to have a twittertype of 3"
#tweetCollection.update({},{"$set":{"tweettype":3}}, multi=True)
#print "done updating db"

result = api.GetListTimeline(list_id=95200241, slug="wrplaying-blogs", count=200)

#result = api.GetListsList("kalisurfer")

#for lists in result:
	#print lists

for tweet in result:
	print "looking to see if we already have the tweet"
	exisiting_tweet = tweetCollection.find_one({"_id": tweet.id})

	score = tweet.favorite_count + tweet.retweet_count + 1
	post = {
			"author": tweet.user.screen_name,
			"text": tweet.text,
			"_id": tweet.id,
			"authorID": tweet.user.id,
			"fav_count": tweet.favorite_count,
			"rt_count": tweet.retweet_count,
			"geo": tweet.geo,
			"created_at": tweet.created_at,
			"score": score,
			"game": 0,
			"tweettype": 2
		}


	if exisiting_tweet:
		print("yep this tweet ", tweet.id, " already exist in our db")
		tweetCollection.update({"_id": tweet.id}, {"$set": {"tweettype": 2}})
	else:
		print("this tweet does not exist ", tweet.id)
		tweetCollection.save(post)
		print(tweet.text)
		print("the authorID was ", tweet.user.id)

				


#listing = gameCollection.find({});

#http://cdn.superbwallpapers.com/wallpapers/games/call-of-duty-ghosts-19880-400x250.jpg

# set of arrays to get games in
# {"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "account":"tesonline", "tags": ["assassin's creed black flag", "acblackflag"]}
# gameCollection.update({}, { "$set": {"trendIndex": 0}}, upsert=False, multi=True)
#results = gameCollection.find({"releaseDate": { "$gt": datetime.datetime.utcnow() }});
#results = gameCollection.find({ "heroURL" : {"$not":{"$regex" : ".*localhost.*"}}});
#results = gameCollection.find({ "heroURL" : {"$regex" : ".*lorempixel.*"}});

#print dir(api)



	#print "the new date is "
	#print newDate
	#print "****** /n"