'''
Created on Sep 28, 2013

Job: grabs all tweets marked as 0 (ie not assigned to a game yet) and puts the tweets out to a coma delimited list
'''
# Dashboard that looks 

import twitter
import csv
import pprint
from datetime import date, timedelta, datetime
import time
import string
import pymongo
from pymongo import MongoClient


def what_are_they_talking_about():
	messages = []
	client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
	db = client.weareplayingit

	# game scaffolding
	tweetCollection = db.tweet

	#talkingAbout = tweetCollection.find({"game": 0, "created_at": {"$gt": "2011-10-01T23:36:08.000Z"}}).sort("score", -1)

	#get all tweets from the last day

	d = datetime.utcnow() - timedelta(hours=2)


	talkingAbout = tweetCollection.find({"game":0, "created_at": {"$gte": d}})

	'''
	talkingAbout = tweetCollection.find({
											"game": 0, 
											"created_at": {
												"$gte": { 
													"$date": start 
														}
													}
												}).sort("created_at", -1)

	'''
	print talkingAbout.count()
	#exit()

	if (talkingAbout.count() > 0):
		print("WE GOT RESULTS.  LIKE ", talkingAbout.count(), " OF THEM")
		with open("tweets.csv", "wb") as outfile:
			csvoutfile = csv.writer(outfile)
			csvoutfile.writerow(["CONTENT"])

			for tweets in talkingAbout:
				csvoutfile.writerow([tweets.get("text").encode("utf-8")])
				# to feed csv

				#print tweets.get("author")
				messages.append(tweets.get("text"))
				#print( tweets.get("author") , ",", tweets.get("text"))
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
		messages.append("NO RESULTS")

	return "\r\n".join(messages)
