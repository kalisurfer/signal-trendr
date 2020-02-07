'''
Created on Dec 2, 2013

@author: varys

Job: Looks at all entries in the game  collection that do not have a youtube channel ID ytChannel.  
Once the list is built, the script loops through it and seeks to add a channelId.  
Youtube channels are used to monitor for new trailers on games we follow.

'''


import csv
#from apiclient.errors import HttpError
import sys
import random, json, time, freebase, urllib
from apiclient.errors import HttpError
import oauth2client.client as Client
import httplib2 as http
from apiclient.discovery import build

from datetime import datetime
import json
import re
import string
from bson.objectid import ObjectId
import pymongo
from pymongo import MongoClient

descriptions = {
	"newvid": "New Video"
}

# START of database items
client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

start = datetime(2013, 10, 20, 1, 0, 0, 100)
now = datetime.utcnow()

# game scaffolding
gameCollection = db.games
tweetCollection = db.tweet
eventCollection = db.event
historyCollection = db.game_history
ytVids = db.video #this will be where trailers will be pulled from in the near future. right now trailers are pulled from the game table using the field trailer

listing = gameCollection.find({"recent_rank": {"$gt": 0}, "ytChannel": {"$ne":None}})
#listing = gameCollection.find({"_id": ObjectId("528b1afee4b0b33de7a6c44b") })


# END of database items

#OPTIONAL
# THIS RUNS THROUGH ALL OF THE TRAILER ROW IN GAME GRABS THE ID AND RETURNS THE CHANNEL ID AND UPDATES THE GAME TABLE WITH IT
# DO THIS FIRST
'''
for listings in listing:
    listing_id = listings.get('_id')
    print listings.get('trailer')
    trailers = listings.get('trailer', [])
    if isinstance(trailers, basestring):
        trailers = [trailers]
    if len(trailers):
        trailer = trailers[0]
        quote = [trailer.split("/")[-1]]
        thing2 = thing1.videos(quote)
        #thing2 = thing1.videos('QkkoHAzjnUs')
        print listing_id, quote
        print thing2
        print "#######################"
        print listings.get('title')
        print listings.get('_id')
        #print thing2[0]['channelId']
        if thing2[0]['id']:
          
          try:
            print thing2[0]['publishedAt']
            gameCollection.update(
              {"_id": listings.get('_id')},
              {"$set": {"ytChannel": thing2[0]['channelId']}})




          except:
            print "problem with publish date"

          try:
            print thing2[0]['channelId']
          except:
            print "problem with channelId"

          try:
            print thing2[0]['title']
          except:
            print "problem 2 with that id"
        else:
          print "problem with that id"
        print "----------------------------------------"
    else:
        print listing_id, "has none"
        print "----------------------------------------"

exit()'''


# This loops through table to to push out CID. Since we pull the channelId inside main now we can do this externally. Ideally, we want to have a scheduler that keeps track of how frequently a page has been updated (so older channels that are inactive don't get the same priority as newer channels)
'''
for listings in listing:
	print "getting videos from this channel ", listings.get('ytChannel')
	try:
		CID = listings.get('ytChannel')
		try:
			queries = [listings.get('tags')] #ideally tags would be for youtube specifically but in this case taking the title
		except:
			print "there was an ERROR retrieving the title tags"
	except:
		print "there was an ERROR retrieving the channelId"
'''

def __save(data):
	print "saving Video"

	#find if the video has been saved before
	existing_video = ytVids.find_one({"videoId": data['videoId']})
	if existing_video:
		print "there already exist a video with that id ", data['videoId']
		return False
	else:
		ytVids.save(data)
		print "video was inserted with id ", data['videoId']
		return True

def __createEvent(type, game):
	print "Creating a new event"
	description = descriptions[type] if type in descriptions.keys() else "Unknown Event"
	print "creating event for ", game
	eventCollection.insert({"dateAdded": now, "type": type, "description": description, "game": ObjectId(game)})

def main(argv = None):
	
	DEVELOPER_KEY = "AIzaSyBmoEe-vqMw-354VifVh2hSbvzgeB7iAgI"
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"
	
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
	
	outdata = []
	ids = []

	if len(argv) > 1:
		print "using channel from table ", argv.get('ytChannel')
		CID = argv.get('ytChannel')
	else:
		print "using default channel"
		CID = 'UCgc4mg2uHQ_vdhLyhtQcgTA' #test channel

	game = gameCollection.find_one({'ytChannel':CID}) #test date
	publishedAfter = ""
	'''if "ytLastUpdate" in argv:
		publishedAfter = argv.get("ytLastUpdate")
	else:	
		publishedAfter = "2013-07-10T01:00:00.000Z"
	'''
	publishedAfter = "2013-06-01T01:00:00.000Z"
	#queries = game["ed_tags"] #test queries
	print "date is ", publishedAfter
	queries = argv["tags"]
	print queries
	print publishedAfter
	more_videos = True
	new_videos = True
	pageToken = None
	newContent = False

	for j in range(len(queries)):
		print "IN QUERIES ", j
		while more_videos and new_videos:
			more_videos = False
			new_videos = False
			thing2 = None
			print "LOOKING FOR THIS ", str(queries[j])
			
			if pageToken is None:
				thing2 = youtube.search().list(
						        part="id,snippet",
						        publishedAfter = publishedAfter,
						        q = str(queries[j]),
						        channelId = CID,
						        type = 'video',
						        maxResults= '50',
						        order = 'date',
						        ).execute()
				print "only after this date", publishedAfter
			else:
				thing2 = youtube.search().list(
						        part="id,snippet",
						        publishedAfter = publishedAfter,
						        q = str(queries[j]),
						        channelId = CID,
						        type = 'video',
						        maxResults= '50',
						        order = 'date',
						        pageToken = pageToken
						        ).execute()
			
			#print thing2['items']
			for item in thing2['items']:
				if 'id' in item and 'title' in item['snippet']:
					#print item['snippet']['title']
					print "hello"
					
					if (not(item['id']['videoId'] in ids)):
						ids.append(item['id']['videoId'])
						try:

							resultSet = {
								'title': item['snippet']['title'],
								'publishedAt': item['snippet']['publishedAt'],
								'videoId': item['id']['videoId'],
								'game': argv.get('_id')

							}
							tempBool = __save(resultSet)

							if tempBool:
								newContent = True

							#print resultSet
							print "saving ", item['snippet']['title']
							'''print item['snippet']['publishedAt']
							print item['snippet']['description']
							print item['id']['videoId']
							print argv.get('_id')
							
								result[item]["title"] = search_result["snippet"]["title"]
      result[item]["publishedAt"] = search_result["snippet"]["publishedAt"]
      result[item]["channelId"] = search_result["snippet"]["channelId"]
      result[item]["description"] = search_result["snippet"]["description"]
      result[item]["id"] = search_result["id"]["videoId"]

							'''
							#thing3[0]['id'] = thing2[i]['id']
							new_videos = True
							outdata.append(item)
						except:
							print "failed"
								
			if 'nextPageToken' in thing2:
				if len(outdata) < 951 and new_videos is True:
					try:
						print thing2['nextPageToken']
						more_videos = True
						pageToken = thing2['nextPageToken']
					except:
						print "failed to get page token"

			print more_videos
			print pageToken
			print new_videos
			print len(outdata)
		
		more_videos = True
		new_videos = True
	
	#check to see if the game had new content
	if newContent:
		__createEvent('newvid', argv.get('_id'))

	#game.update({"_id":game["_id"]},{"ytLastUpdate":outdata[0]["snippet"]["publishedAt"]})
	#print outdata
	print "ytVids.insert(outdata,continue_on_error = True)"
	#ytVids.insert(outdata,continue_on_error = True)

print "count is ", listing.count()
for listings in listing:
	print "in listings"
	main(listings)

'''if __name__ == '__main__':
	main(sys.argv)
'''