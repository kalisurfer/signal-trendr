'''
Created on Jan 15, 2013
@author: varys

Job: Looks at all entries in the game  collection that do not have a youtube channel ID ytChannel.  
Once the list is built, the script loops through it and seeks to add a channelId.  
Youtube channels are used to monitor for new trailers on games we follow.

'''
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

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

start = datetime(2013, 10, 20, 1, 0, 0, 100)

# game scaffolding
gameCollection = db.games
tweetCollection = db.tweet
historyCollection = db.game_history
ytVids = db.video

listing = gameCollection.find({"ytChannel": None});

#from optparse import OptionParser

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your project.
def parse_date(date_string):
  return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

class FreebaseRequests():
  
  def __init__(self):
    self.DEVELOPER_KEY = "AIzaSyBmoEe-vqMw-354VifVh2hSbvzgeB7iAgI"
    self.FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"
    
    
  def get_topic_ids(self,options):
    freebase_params = dict(query=options.query, key=self.DEVELOPER_KEY)
    freebase_url = self.FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
    freebase_response = json.loads(urllib.urlopen(freebase_url).read())
    
    if len(freebase_response["result"]) == 0:
      exit("No matching terms were found in Freebase.")

    mids = []
    index = 1
    print "The following topics were found:"
    for result in freebase_response["result"]:
      if result["score"] > 50:
        mids.append(result["mid"])
        print "  %2d. %s (%s)" % (index, result.get("name", "Unknown"),
          result.get("notable", {}).get("name", "Unknown"))
        index += 1
  
    return mids

  
  def get_id_details(self,query):
    print "try again later"

class YouTubeRequests():
  
  def __init__(self):
    self.DEVELOPER_KEY = "AIzaSyBmoEe-vqMw-354VifVh2hSbvzgeB7iAgI"
    self.YOUTUBE_API_SERVICE_NAME = "youtube"
    self.YOUTUBE_API_VERSION = "v3"

  def videos(self,queries):
    '''
      Takes an array of video IDs and returns the stats and Freebase topic IDs for those videos.
    '''
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
    developerKey=self.DEVELOPER_KEY)
    result = []
    ids = ""
    
    for video in queries:
      ids = ids +","+ video
      result.append({'id':video, 'type':'video'})
      
    response = youtube.videos().list(
      part="snippet,statistics,topicDetails",
      id=ids,
      ).execute()
      
    item = 0
    for search_result in response.get("items", []):
      result[item]["title"] = search_result["snippet"]["title"]
      try:
        result[item]["topicIds"] = search_result["topicDetails"]["topicIds"]
      except:
        result[item]["topicIds"] = []
      result[item]["publishedAt"] = search_result["snippet"]["publishedAt"]
      result[item]["channelId"] = search_result["snippet"]["channelId"]
      result[item]["description"] = search_result["snippet"]["description"]
      result[item]["statsTime"] = time.time()
      result[item]["viewCount"] = search_result["statistics"]["viewCount"]
      result[item]["likeCount"] = search_result["statistics"]["likeCount"]
      result[item]["dislikeCount"] = search_result["statistics"]["dislikeCount"]
      result[item]["commentCount"] = search_result["statistics"]["commentCount"]
      item += 1
      
    return result
  
  def search(self,options):
    '''Don't look at this, it's hideous. 
        However, it *will* take any options you want, construct a proper API call, and get you results. 
        The last item returned is either the last item on the list or the link to the next page. Not sure if you're done?
        Check the last item.
    '''
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
    developerKey=self.DEVELOPER_KEY)
    switch = 15
    
    #Check/Set Defaults
    if("publishedAfter" not in options):
      options["publishedAfter"] = "1970-01-01T00:00:00Z"
    if("publishedBefore" not in options):
      year,mon,day,hour,minut,sec,x1,x2,x3 = time.localtime()
      if mon < 10:
        options["publishedBefore"] = str(year)+"-0"+str(mon)+"-"+str(day)+"T"+str(hour)+":"+str(minut)+":"+str(sec)+"Z"
      else:
        options["publishedBefore"] = str(year)+"-"+str(mon)+"-"+str(day)+"T"+str(hour)+":"+str(minut)+":"+str(sec)+"Z"
    if("q" not in options):
      print "no q"
      switch = switch - 8
      print switch
    if("channelId" not in options):
      switch = switch - 4
      print switch
    if("topicId" not in options):
      switch = switch - 2
    if("type" not in options):
      options["type"] = "video"
    if("maxResults" not in options):
      options["maxResults"] = 25
    if("order" not in options):
      options["order"] = "relevance"
    if("pageToken" not in options):
      switch = switch - 1
    
    result = []
    #TODO: parse missing values better. Seriously, this is an awful chunk of code
    if(switch < 8):
      if(switch < 4):
        if(switch < 2):
          if(switch == 1):
            response = youtube.search().list(
              part="id,snippet",
              publishedAfter = options["publishedAfter"],
              publishedBefore = options["publishedBefore"],
              type = options["type"],
              maxResults= options["maxResults"],
              order = options["order"],
              pageToken = options["pageToken"]
              ).execute()
          else: #switch is 0
            response = youtube.search().list(
              part="id,snippet",
              publishedAfter = options["publishedAfter"],
              publishedBefore = options["publishedBefore"],
              type = options["type"],
              maxResults= options["maxResults"],
              order = options["order"]
              ).execute()
        elif(switch == 2):
          response = youtube.search().list(
            part="id,snippet",
            publishedAfter = options["publishedAfter"],
            publishedBefore = options["publishedBefore"],
            type = options["type"],
            maxResults= options["maxResults"],
            order = options["order"],
            topicId = options["topicId"]
            ).execute()
        else: #switch is 3
          response = youtube.search().list(
            part="id,snippet",
            publishedAfter = options["publishedAfter"],
            publishedBefore = options["publishedBefore"],
            type = options["type"],
            maxResults= options["maxResults"],
            order = options["order"],
            topicId = options["topicId"],
            pageToken = options["pageToken"]
            ).execute()
      elif(switch < 6):
        if(switch == 5):
          response = youtube.search().list(
            part="id,snippet",
            publishedAfter = options["publishedAfter"],
            publishedBefore = options["publishedBefore"],
            channelId = options["channelId"],
            type = options["type"],
            maxResults= options["maxResults"],
            order = options["order"],
            pageToken = options["pageToken"]
            ).execute()
        else: #switch is 4
          response = youtube.search().list(
            part="id,snippet",
            publishedAfter = options["publishedAfter"],
            publishedBefore = options["publishedBefore"],
            channelId = options["channelId"],
            type = options["type"],
            maxResults= options["maxResults"],
            order = options["order"]
            ).execute()
      elif(switch == 6):
        response = youtube.search().list(
          part="id,snippet",
          publishedAfter = options["publishedAfter"],
          publishedBefore = options["publishedBefore"],
          channelId = options["channelId"],
          topicId = options["topicId"],
          type = options["type"],
          maxResults= options["maxResults"],
          order = options["order"]
          ).execute()
      else: #switch is 7
        response = youtube.search().list(
          part="id,snippet",
          publishedAfter = options["publishedAfter"],
          publishedBefore = options["publishedBefore"],
          channelId = options["channelId"],
          topicId = options["topicId"],
          type = options["type"],
          maxResults= options["maxResults"],
          order = options["order"],
          pageToken = options["pageToken"]
          ).execute()
    elif(switch < 12):
      if(switch < 10):
        if(switch == 9):
          response = youtube.search().list(
            part="id,snippet",
            publishedAfter = options["publishedAfter"],
            publishedBefore = options["publishedBefore"],
            q = options["q"],
            type = options["type"],
            maxResults= options["maxResults"],
            order = options["order"],
            pageToken = options["pageToken"]
            ).execute()
        else: #switch is 8
          response = youtube.search().list(
            part="id,snippet",
            publishedAfter = options["publishedAfter"],
            publishedBefore = options["publishedBefore"],
            q = options["q"],
            type = options["type"],
            maxResults= options["maxResults"],
            order = options["order"],
            ).execute()
      elif(switch == 10):
        response = youtube.search().list(
          part="id,snippet",
          publishedAfter = options["publishedAfter"],
          publishedBefore = options["publishedBefore"],
          q = options["q"],
          topicId = options["topicId"],
          type = options["type"],
          maxResults= options["maxResults"],
          order = options["order"],
          ).execute()
      else: #switch is 11
        response = youtube.search().list(
          part="id,snippet",
          publishedAfter = options["publishedAfter"],
          publishedBefore = options["publishedBefore"],
          q = options["q"],
          topicId = options["topicId"],
          type = options["type"],
          maxResults= options["maxResults"],
          order = options["order"],
          pageToken = options["pageToken"]
          ).execute()
    elif(switch < 14):
      if(switch == 13):
        response = youtube.search().list(
          part="id,snippet",
          publishedAfter = options["publishedAfter"],
          publishedBefore = options["publishedBefore"],
          q = options["q"],
          channelId = options["channelId"],
          type = options["type"],
          maxResults= options["maxResults"],
          order = options["order"],
          pageToken = options["pageToken"]
          ).execute()
      elif(switch == 12):
        response = youtube.search().list(
          part="id,snippet",
          publishedAfter = options["publishedAfter"],
          publishedBefore = options["publishedBefore"],
          q = options["q"],
          channelId = options["channelId"],
          type = options["type"],
          maxResults= options["maxResults"],
          order = options["order"]
          ).execute()
    elif(switch < 15): #switch is 14
      response = youtube.search().list(
        part="id,snippet",
        publishedAfter = options["publishedAfter"],
        publishedBefore = options["publishedBefore"],
        q = options["q"],
        channelId = options["channelId"],
        topicId = options["topicId"],
        type = options["type"],
        maxResults= options["maxResults"],
        order = options["order"]
        ).execute()
    else: #switch is 15
      response = youtube.search().list(
        part="id,snippet",
        publishedAfter = options["publishedAfter"],
        publishedBefore = options["publishedBefore"],
        q = options["q"],
        channelId = options["channelId"],
        topicId = options["topicId"],
        type = options["type"],
        maxResults= options["maxResults"],
        order = options["order"],
        pageToken = options["pageToken"]
        ).execute()
    
    item = 0
    for search_result in response.get("items", []):
      result.append({})
      result[item]["title"] = search_result["snippet"]["title"]
      result[item]["publishedAt"] = search_result["snippet"]["publishedAt"]
      result[item]["channelId"] = search_result["snippet"]["channelId"]
      result[item]["description"] = search_result["snippet"]["description"]
      result[item]["id"] = search_result["id"]["videoId"]
      item += 1
      
    if "nextPageToken" in response:
      result.append({'nextPageToken':response.get('nextPageToken',None)})
      
    return result


  def playlist(self,queries):
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
    developerKey=self.DEVELOPER_KEY)
		
    #loop through passed array
    for playlist in queries:
      miniResults = {}
      uri = playlist+"&alt=json"
      print uri
      resp, rawData = http.Http().request(uri)
      print resp.status
      miniResults["type"] = "playlist"
      miniResults["entry"] = [];

      try:
        v2data = json.loads(rawData)
        #print v2data
        #print v2data['feed']['entry']
        for n in range(0,len(v2data['feed']['entry'])):
          miniResult = {}
          thedata = v2data['feed']['entry'][n]
          #print miniResult
          miniResult = {
            'title': thedata['title']['$t'],
            'uploadedAt': parse_date(thedata['media$group']['yt$uploaded']['$t']),
            'videoId': thedata['media$group']['yt$videoid']['$t'],
            'videoDuration': thedata['media$group']['yt$duration']['seconds'],
            #'viewCount': thedata['yt$statistics']['viewCount']
            }
          
          miniResults["entry"].append(miniResult)
          print miniResults["entry"][n]
          print "****&&***********&&&****"

        return miniResults

      except NameError as e:
        print "there was an issue with loading the data ", e
        return e
       
  def channels(self,queries):
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
    developerKey=self.DEVELOPER_KEY)
    result = []
    results = []
    ids = ""
    foundResults = 0
    
    for channel in queries:
      miniResult = {}
      uri = "http://gdata.youtube.com/feeds/api/users/"+channel+"?v=200&alt=json"
      print uri
      resp, rawData = http.Http().request(uri)
      print resp.status
      try:  
        v2data = json.loads(rawData)
        miniResult["type"] = "channel"
        miniResult["summary"] = v2data["entry"]["summary"]["$t"]
        miniResult["name"] = v2data["entry"]["yt$username"]["$t"]
        miniResult["viewCount"] = v2data["entry"]["yt$statistics"]["totalUploadViews"]
        miniResult["publishedAt"] = v2data.get("entry").get("published").get("$t")
        miniResult["updatedAt"] = v2data.get("entry").get("updated").get("$t") #last time channel was updated
        miniResult["playlist"] = v2data["entry"]["gd$feedLink"][6]["href"]
        miniResult["subscriberCount"] = v2data["entry"]["yt$statistics"]["subscriberCount"]
        miniResult["id"] = v2data["entry"]["yt$channelId"]["$t"]
        miniResult["statsTime"] = time.time()
        result.append(miniResult);
        ids = ids +","+ v2data["entry"]["yt$channelId"]["$t"]
        foundResults += 1
      except:
        if (resp.status is 403) or (resp.status is "403"):
          raise HttpError( "quotaExceeded" )
      
      #miniResult["id"] = v2data["entry"]["yt$channelId"]["$t"]
    while foundResults > 0:
      response = youtube.channels().list(
        part="id,topicDetails,statistics",
        id=ids,
        maxResults=50
        ).execute()
      results.extend(response.get("items",[]))
      foundResults = foundResults - 50
      
    for n in range(0,len(results)):
      result[n]["topicIds"] = results[n]["topicDetails"]["topicIds"]
      result[n]["videoCount"] = results[n]["statistics"]["videoCount"]
    print result
    return result
  
  def playlists(self,queries, playlists = [],plnum = 0):
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,developerKey=self.DEVELOPER_KEY)

    next_page_token = ''
    if plnum >= len(queries):
			return playlists
	
    if "pages" not in queries[plnum]:
    	queries[0]["pages"] = []
	
    if "pageToken" in queries[plnum]:
    	next_page_token = queries[plnum]["pageToken"]

    playlistitems_response = youtube.playlists().list(channelId=queries[plnum]["channelId"],part='snippet',maxResults=50,pageToken=next_page_token).execute()
    
    for playlist_item in playlistitems_response['items']:
      #print playlist_item
      print "**********************************************************************"
      print playlist_item["id"]
      print "**********************************************************************"


      playlists.append(playlist_item["id"])

    if 'nextPageToken' in playlistitems_response:
    	next_page_token = playlistitems_response['nextPageToken']
    	if ( next_page_token not in queries[plnum]["pages"] ) and (len(playlists) < playlistitems_response['pageInfo']['totalResults']):
    		 queries[plnum]["pages"].append(next_page_token)
    		 queries[plnum]["pageToken"] = next_page_token
    		 return self.playlists(queries,playlists,plnum)
    	else:
    		if plnum < len(queries):
    			return self.playlists(queries,playlists,plnum+1)
    		else:
    			return playlists
    else:
    	if plnum < len(queries):
    		return self.playlists(queries,playlists,plnum+1)
    	else:
    	  return playlists
  
  def __saveVideo(self, video):
    print "called __saveVideo"
    try:
      ytVids.save(video)
    except:
      print "error inserting video"
      print "%^%^%^%^%^%^%^%^%^%^%"
      print video
      print "^&^&^&^&^&^&^&^&^&^&^"



  def playlistItems(self,queries, videos = [],plnum = 0):
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,developerKey=self.DEVELOPER_KEY)

    next_page_token = ''
    if plnum >= len(queries):
			return videos
	
    if "pages" not in queries[plnum]:
    	queries[0]["pages"] = []
	
    if "pageToken" in queries[plnum]:
    	next_page_token = queries[plnum]["pageToken"]

    playlistitems_response = youtube.playlistItems().list(playlistId=queries[plnum]["playlistId"],part='snippet',maxResults=50,pageToken=next_page_token).execute()
    
    for playlist_item in playlistitems_response['items']:
      #print playlist_item
      #print "**********************************************************************"

      miniResult = {
            'title': playlist_item['snippet']['title'],
            'uploadedAt': parse_date(playlist_item['snippet']['publishedAt']),
            '_id': playlist_item['snippet']['resourceId']['videoId'],
            #'videoDuration': playlist_item['media$group']['yt$duration']['seconds'],
            #'viewCount': thedata['yt$statistics']['viewCount']
            }
      #print "printing miniResult"
      #print miniResult
      #print "**********************************************************************"

      self.__saveVideo(miniResult)


      videos.append(playlist_item)

    if 'nextPageToken' in playlistitems_response:
    	next_page_token = playlistitems_response['nextPageToken']
    	if ( next_page_token not in queries[plnum]["pages"] ) and (len(videos) < playlistitems_response['pageInfo']['totalResults']):
    		 queries[plnum]["pages"].append(next_page_token)
    		 queries[plnum]["pageToken"] = next_page_token
    		 return self.playlistItems(queries,videos,plnum)
    	else:
    		if plnum < len(queries):
    			return self.playlistItems(queries,videos,plnum+1)
    		else:
    			return videos
    else:
    	if plnum < len(queries):
    		return self.playlistItems(queries,videos,plnum+1)
    	else:
    	  return videos
  
  def makeRequest(self,qType,queries,options = None):
    '''Requests YouTube Data API v3 replies. Can search for things, list channels, and list videos'''
    #Client.credentials_from_code(client_id, client_secret, scope, code, redirect_uri, http, user_agent, token_uri)
    if qType is "video":
      return self.videos(queries)
    elif qType is "channel":
      return self.channels(queries)
    elif qType is "search":
      return self.search(options)
    elif qType is "playlistItems":
    	return self.playlistItems(queries)
    elif qType is "playlists":
    	return self.playlists(queries)
    else:
      print "improper request"
      return None
    # assert resp.status == '200'
    
  
  def makeRequestWithExponentialBackoff(self,qType,queries = [],options = None):
    '''This takes requests and gracefully backs off if we hit a quota cap of some kind rather than hammering the server'''
    for n in range(0, 5):
      try:
        return self.makeRequest(qType,queries,options)
          
      except HttpError, error:
        print error
        print HttpError
        if (error.resp.reason in ['userRateLimitExceeded', 'quotaExceeded']) or (HttpError.message is "quotaExceeded"): 
          print "sleeping because we exceeded rate limit"
          time.sleep((2 ** n) + (random.randint(0, 1000) / 1000))
      
    return "There has been an error, the request never succeeded."
  
  def v2comments(self,query,options):
    #youtube = build(self.YOUTUBE_API_SERVICE_NAME, "v2",developerKey=self.DEVELOPER_KEY)
    uri = ""
    vid = query["id"]
    if "next" in options:
      uri = options["next"]
    else:
      uri = "http://gdata.youtube.com/feeds/api/videos/"+vid+"/comments?alt=json"
    print uri
    
    resp, rawData = http.Http().request(uri)
    print resp.status
    result = json.loads(rawData)
    for link in result["feed"]["link"]:
      print link["href"]
      print link["rel"]
      if "next" in link["rel"]:
        result["next"] = link["href"]
        print result["next"]
    return result
  
  def makeV2Request(self,qType,queries,options = None):
    '''Requests YouTube Data API v3 replies. Can search for things, list channels, and list videos'''
    #Client.credentials_from_code(client_id, client_secret, scope, code, redirect_uri, http, user_agent, token_uri)
    if qType is "comments":
      return self.v2comments(queries[0],options)
    else:
      print "improper request"
      return None
    # assert resp.status == '200'
  
  def makeV2RequestWithExponentialBackoff(self,qType,queries = [],options = None):
    '''This takes requests and gracefully backs off if we hit a quota cap of some kind rather than hammering the server'''
    for n in range(0, 5):
      try:
        return self.makeV2Request(qType,queries,options)
          
      except HttpError, error:
        print error
        print HttpError
        if (error.resp.reason in ['userRateLimitExceeded', 'quotaExceeded']) or (HttpError.message is "quotaExceeded"): 
          print "sleeping because we exceeded rate limit"
          time.sleep((2 ** n) + (random.randint(0, 1000) / 1000))
      
    return "There has been an error, the request never succeeded."


#quote = ['d4JnshyKOOQ'];
thing1 = YouTubeRequests()
#thing2 = thing1.makeRequest("search", "search",{'q':'Dead Space 3','channelId':'UCLCmJiSbIoa_ZFiBOBDf6ZA'})
#thing2 = thing1.makeRequest("search", "search",{'videoId':'d4JnshyKOOQ'})
#thing2 = thing1.videos(quote)

# THIS IS FUGLY | PLeASE DO NOT JUDGE ME



# THIS RUNS THROUGH ALL OF THE TRAILER ROW IN GAME GRABS THE ID AND RETURNS THE CHANNEL ID AND UPDATES THE GAME TABLE WITH IT
# DO THIS FIRST

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

exit()
'''
# THIS RUNS THROUGH ALL OF THE CHANNEL IN GAME AND PULLS THE VIDEOS
# DO THIS SECOND
for listings in listing:
  try:
    ytChannel = listings.get('ytChannel')
    if ytChannel:
      print ytChannel
      quote = [ytChannel]
      thing2 = thing1.channels(quote)
      print thing2
      print "#######################"
      print thing2[0]['playlist']
      print thing2[0]['updatedAt']

      try:
        gameCollection.update(
              {"_id": listings.get('_id')},
              {"$set": {"ytPlaylist": thing2[0]['playlist'], "ytLastUpdate": thing2[0]['updatedAt'] }})
              #{"$set": {"ytPlaylist": thing2[0]['playlist'], "ytLastUpdate": datetime.strptime(thing2[0]['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ") }})
      except:
        print "error inserting playlist and updatedAt"

      print "------------------------------------------------"
    else:
      print "there was an issue with the channel ie it was none"



  except:
    print "there was an issue with the channel"
'''

# THIS RUNS THROUGH THE PLAYLIST AND GRABS ALL VIDEOS
# DO THIS THIRD

i = 0


									
'''
exit()
'''
for listings in listing:
  if (listings.get('ytChannel')):
    if (i > 4):
      quote = [listings.get('ytChannel')]
      playlists = []
      taco1 = thing1.makeRequestWithExponentialBackoff('playlists', queries = [{'channelId': listings.get('ytChannel')}])
      for playlist in taco1:
        playlists.append({'playlistId':playlist})

      taco2 = thing1.makeRequestWithExponentialBackoff('playlistItems', queries = playlists)
      print i
      print listings.get('ytChannel')
      print listings.get('title')
      print "###########################################################"
      quote = [{'playlistId': listings.get('ytPlaylist')}]
      thing2 = thing1.makeRequestWithExponentialBackoff('playlistItems', queries = quote)
    i = i + 1

print "i is the greatest and it is " + i
#quote = ['http://gdata.youtube.com/feeds/api/users/battlefield/uploads?v=2']
#thing2 = thing1.playlist(quote)