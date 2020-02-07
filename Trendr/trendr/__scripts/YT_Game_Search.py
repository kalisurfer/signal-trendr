'''
Created on Dec 2, 2013

@author: varys
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

def main(argv = None):
	

	client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
	db = client.weareplayingit
	
	start = datetime(2013, 10, 20, 1, 0, 0, 100)
	
	# game scaffolding
	gameCollection = db.games
	tweetCollection = db.tweet
	historyCollection = db.game_history
	ytVids = db.video
	
	listing = gameCollection.find({});
	DEVELOPER_KEY = "AIzaSyBmoEe-vqMw-354VifVh2hSbvzgeB7iAgI"
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"
	
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
	
	outdata = []
	ids = []

	if len(argv) > 1:
		CID = argv[1]
	else:
		print "using default channel"
		CID = 'UCgc4mg2uHQ_vdhLyhtQcgTA' #test channel
	game = gameCollection.find_one({'ytChannel':CID}) #test date
	publishedAfter = ""
	if "ytLastUpdate" in game:
		publishedAfter = game["ytLastUpdate"]
	else:	
		publishedAfter = "2010-10-10T01:00:00.000Z"

	queries = game["ed_tags"] #test queries
	print queries
	print publishedAfter
	more_videos = True
	new_videos = True
	pageToken = None

	for j in range(len(queries)):
		while more_videos and new_videos:
			more_videos = False
			new_videos = False
			thing2 = None
			
			if pageToken is None:
				thing2 = youtube.search().list(
						        part="id,snippet",
						        publishedAfter = publishedAfter,
						        q = queries[j],
						        channelId = CID,
						        type = 'video',
						        maxResults= '50',
						        order = 'date',
						        ).execute()
			else:
				thing2 = youtube.search().list(
						        part="id,snippet",
						        publishedAfter = publishedAfter,
						        q = queries[j],
						        channelId = CID,
						        type = 'video',
						        maxResults= '50',
						        order = 'date',
						        pageToken = pageToken
						        ).execute()
			
			print thing2['items']
			for item in thing2['items']:
				if 'id' in item and 'title' in item['snippet']:
					print item['snippet']['title']
					if (not(item['id']['videoId'] in ids)):
						ids.append(item['id']['videoId'])
						try:
							print item['snippet']['title']
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
	
	game.update({"_id":game["_id"]},{"ytLastUpdate":outdata[0]["snippet"]["publishedAt"]})
	print "ytVids.insert(outdata,continue_on_error = True)"
	#ytVids.insert(outdata,continue_on_error = True)

if __name__ == '__main__':
	main(sys.argv)