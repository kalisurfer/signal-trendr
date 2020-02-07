'''
Created on Feb 7, 2013

@author: varys
'''

'''
//AIzaSyBmoEe-vqMw-354VifVh2hSbvzgeB7iAgI - key
var key;
var vidDb;

function setglobals() {
  key = "AIzaSyBmoEe-vqMw-354VifVh2hSbvzgeB7iAgI";
  vidDb = ScriptDb.getMyDb();
  channelData_URI = "http://gdata.youtube.com/feeds/api/users/" #add username and "?v=2&alt=json"
  playlist_URI = ##
  video_URI = 
}
'''

import json, requests, re, csv, MySQLdb
#from apiclient.errors import HttpError
#import random, time, sys
import oauth2client.client as Client
from Backoff_Requests import YouTubeRequests

class WebStuff():
  
  def __init__(self):
    self.db_connect = MySQLdb.connect(host = "localhost",
                        user = "root",
                        passwd = "pleasestop",
                        db = "Vlogger_Campaign_Db",
                        charset = "utf8",
                        use_unicode = True)

  def GetSocialBladeData(self,uname,channel = 'youtube'):
    query = "http://socialblade.com/"+channel+"/user/" + uname
    result = requests.get(query)
    n = re.search('(?<=network/)[a-zA-Z0-9]+',result.text)
    network = n.group(0)
    if network:
      return network
    else:
      return "no network"
  
  def GetFacebookPageData(self,pageName):
    query = "http://graph.facebook.com/"+pageName
    result = requests.get(query)
    parsed = json.loads(result.text)
    print parsed["likes"]
  
class YouTubeStuff():

  def __init__(self):
    self.db_connect = MySQLdb.connect(host = "localhost",
                        user = "root",
                        passwd = "pleasestop",
                        db = "tweet_db",
                        charset = "utf8",
                        use_unicode = True)
    
    
  def UpdateChannelsFromCSV(self,csvfilename = 'Vloggers.csv', people = False,output = True):
    '''
    grab channels from a csv file then pulls and stores their data in SQL db
    '''
    with open(csvfilename, 'rb') as csvfile:
      vloggers = csv.DictReader(csvfile, dialect='excel')
      fields = vloggers.fieldnames
      cursor = self.db_connect.cursor()
      channels = []
      Names = []
      if ("YT_UID" in fields) and (("Real Name" in fields)and(people is True)):
        Requests = YouTubeRequests()
        
        for vlogger in vloggers:
          thisName = []
          if len(vlogger["YT_UID"]) > 15:
            channels.append( vlogger["YT_UID"] )
            name = vlogger["Real Name"].partition(" ")
            thisName.append(name[0])
            if(len(name) == 3):
              thisName.append(name[2])
            elif(len(name) > 3):
              thisName.append(name[len(name)-1])
            else:
              thisName.append("N/A")
            Names.append(thisName)
        
        #Do we know or care about the people listed in this csv?
        if people == True:
          cursor.executemany("INSERT INTO Vlogger_Campaign_Db.Person (First_Name,Last_Name) VALUES (%s,%s)",(Names))
        
        #Grab relevant YT channel data
        results = Requests.makeRequestWithExponentialBackoff("channel", channels)
        
        #if we want to output this data, write it to an output csv
        if output == True:
          csvoutfile = open('Output'+csvfilename, 'wb')
          writer = csv.DictWriter(csvoutfile,fields)
          writer.writeheader()
          writer.writerows(results)
          
        #Okay, this is to avoid SQL injection. Theoretically I could have just used string interpolation and saved execution time, but this is safer.
        for n in range(0,len(results)):
          print results[n]["id"]
          cursor.execute("INSERT INTO Vlogger_Campaign_Db.YouTube_Channel (ChannelID,Name,Description,Subscribers,TotalViews,TotalVideos,PublishedDate,LastUpdated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE (Subscribers,TotalViews,TotalVideos,LastUpdated) = VALUES(Subscribers,TotalViews,TotalVideos,LastUpdated)",
                             (results[n]["id"],
                              results[n]["name"],
                              results[n]["summary"],
                              results[n]["subscriberCount"],
                              results[n]["viewCount"],
                              results[n]["videoCount"],
                              results[n]["publishedAt"],
                              results[n]["statsTime"]))
        self.db_connect.commit()
    
  def ImportChannelsFromDriveFile(self,DriveObject):
    count = 0
    count +=1
    '''grab channels from google doc exports or pulls and store their data in SQL db'''
    #url = "https://www.googleapis.com/youtube/v3/search"
    return
      
  def ListVideos(self,query):
    
    count = 1
    count +=1
    
  def ExportVideos(self,query):
    
    count = 2
    count +=1  
    
  def ExportChannels(self,query):
    
    count = 2
    count +=1  

  '''
  'Finds the channel ID and stats via the YouTube 2.0 API.
  'Finds topicIDs via the YouTube 3.0 Data API.
  '''
  def getChannelStatsByName (self,query):
    return
  '''
  'Finds the channel name, stats, and topicIDs via the YouTube 3.0 Data API.
  'Uses channel name to pull total views and anything missing from 3.0
  '''
  def getChannelStatsById (self,channelId, query = None):
    
    count = 0
    count +=1
    
  '''
  'Scrapes video stats matching the Video ID from the YT 3.0 Data API.
  '''
  def getRelevantVideos (self,channelName,channelId,publishedAfter,query="asdf", topicIds = ["/m/0j_4sm4","/m/05zrxw"],pageToken = None):
    thing1 = YouTubeRequests()
    print channelName
    results = []
    ids = []
    can_continue = True
    should_continue = True
    
    while can_continue and should_continue:
        can_continue = False
        should_continue = False
        thing2 = None
        if pageToken is None:
            thing2 = thing1.makeRequestWithExponentialBackoff("search", ["search"],{'q':query,'channelId':channelId,'publishedAfter':publishedAfter})
        else:
            thing2 = thing1.makeRequestWithExponentialBackoff("search", ["search"],{'q':query,'channelId':channelId,'publishedAfter':publishedAfter,'pageToken':pageToken})
          
        for i in range(len(thing2)):
            if 'id' in thing2[i]:
                thing3 = thing1.makeRequestWithExponentialBackoff("video",[thing2[i]['id']])
                for topicId in topicIds:
                    if (topicId in thing3[0]['topicIds'] or query in thing3[0]['title']) and not (thing2[i]['id'] in ids):
                        ids.append(thing2[i]['id'])
                        should_continue = True
                        print thing3[0]['title']
                        thing3[0]["channelName"] = channelName
                        results.append(thing3[0])
                        break
                
            elif 'nextPageToken' in thing2[i]:
                can_continue = True
                pageToken = thing2[i]['nextPageToken']
    return results
    
  def findVideosByTopic (self,query, topicId = None, channelId = None):
    
    count = 2
    count +=1
  
  def recallVideosByTopic (self,topicId):
    
    count = 3
    count +=1
   

anchor = YouTubeRequests()
outdata = []
fieldnames = []
ids = []
queries = ['Battlefield 4 moments','only in battlefield']
#queries = ['/m/01sjng','/m/0kj4zz_','/m/0gk_mqh','/m/02ks74','/m/02cl3m','/m/06j11d']
topics = ["/m/0vzrw5n","/m/064krrv","/m/0cc7732"]
rtype = ['q','q']
order = 'viewCount'
can_continue = True
should_continue = True
checksum2 = 0
checksum = 0
pageToken = None
titles = ['battlefield','bf3','bf4','moments','only in battlefield']
print len(queries)
channels = []

while can_continue and should_continue:
    can_continue = False
    should_continue = False
    thing2 = None
    if pageToken is None:
        print rtype[checksum]
        print queries[checksum]
        thing2 = anchor.makeRequestWithExponentialBackoff("search",["search"],{rtype[checksum]:queries[checksum],'publishedAfter':'2013-09-18T23:00:00Z','order':order,'maxResults':'50'})
    else:
        print checksum
        thing2 = anchor.makeRequestWithExponentialBackoff("search", ["search"],{rtype[checksum]:queries[checksum],'publishedAfter':'2013-09-18T23:00:00Z','pageToken':pageToken,'order':order,'maxResults':'50'})
    
    for i in range(len(thing2)):
        if 'id' in thing2[i] and 'title' in thing2[i]:
            thing3 = anchor.makeRequestWithExponentialBackoff("video",[thing2[i]['id']])
            if ('topicIds' in thing3[0]) and ('title' in thing3[0]): 
                for title in titles:
                    if (not(thing2[i]['id'] in ids)):
                        ids.append(thing2[i]['id'])
                        try:
                            print thing3[0]['title']
                            should_continue = True
                            outdata.append(thing3[0])
                            channels.append(thing3[0]['channelId'])
                            checksum = True
                        except:
                            print "failed"
                for topic in topics:
                    if (((topic in thing3[0]['topicIds'])) and not(thing2[i]['id'] in ids)):
                        ids.append(thing2[i]['id'])
                        should_continue = True
                        print thing3[0]['title']
                        outdata.append(thing3[0])
                        channels.append(thing3[0]['channelId'])
                        checksum = True
        elif 'nextPageToken' in thing2[i]:
            if len(outdata) < 951 and should_continue is True:
                can_continue = True
                pageToken = thing2[i]['nextPageToken']
            '''elif checksum2 < len(queries) - 1:
                should_continue = True
                can_continue = True
                checksum2 = checksum + 1
                pageToken = None
                query = "race"'''
        
    print can_continue
    print pageToken
    print should_continue
    print len(outdata)

csvoutfile = open('OIB3.csv','wb')
for key in outdata[0].iterkeys():
  fieldnames.append(key)
  print "wrote one"
writer = csv.DictWriter(csvoutfile,fieldnames)
writer.writeheader()
writer.writerows(outdata)
print "wrote stuff"
print channels


'''
anchor = YouTubeRequests()

#Client.flow_from_clientsecrets(filename, scope, redirect_uri, message, cache)
outdata = []
fieldnames = []
ids = []
queries = [{"id":'kQx5MmlP-sg'}]
can_continue = True
lastcall = {}
entries = []

while can_continue:
  can_continue = False
  thing2 = None
  thing2 = anchor.makeV2RequestWithExponentialBackoff("comments",queries,lastcall)
  if len(outdata) > 0:
    outdata.extend(thing2["feed"]["entry"])
  else:
    outdata = thing2["feed"]["entry"]
  if "next" in thing2:
    can_continue = True
    lastcall["next"] = thing2["next"]
  print can_continue
  print len(outdata)

csvoutfile = open('simschat.csv','wb')
for key in outdata[0].iterkeys():
  fieldnames.append(key)
  print "wrote one"
writer = csv.DictWriter(csvoutfile,fieldnames)
writer.writeheader()
writer.writerows(outdata)
print "wrote stuff"
'''

'''
james = YouTubeStuff()
outdata = []
fieldnames = []
channel = []
totalviews = 0
with open('Vloggers.csv', 'rb') as csvfile:
  spamreader = csv.DictReader(csvfile, dialect='excel')
  for row in spamreader:
    newdata = james.getRelevantVideos(row["YouTuber Name"],row["YT_UID"], "2013-02-05T00:00:00Z")
    outdata = outdata + newdata
    
  
csvoutfile = open('voutput.csv','wb')
for key in outdata[0].iterkeys():
  fieldnames.append(key)

writer = csv.DictWriter(csvoutfile,fieldnames)
writer.writeheader()
writer.writerows(outdata)

csvoutfile.close()
'''

'''
steve = james.getRelevantVideos()
print steve
bob = WebStuff()
print bob.SocialBladeData()
bob.FacebookPageData()'''

'''
start = YouTubeStuff()
start.ImportChannelsFromCSV("Vloggers-short.csv")
'''
