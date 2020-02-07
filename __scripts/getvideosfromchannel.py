import json, requests, re, csv, MySQLdb
import oauth2client.client as Client
from Backoff_Requests import YouTubeRequests

anchor = YouTubeRequests()
outdata = []
fieldnames = []
ids = []

#Put channel ID Here
#
#
queries = ['channel1','channel2']
#
#
#

rtype = ['channelId','channelId']
order = 'viewCount'
can_continue = True
should_continue = True
checksum2 = 0
checksum = 0
pageToken = None
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
	        if ('topicIds' in thing3[0]) or ('title' in thing3[0]): 
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
        elif 'nextPageToken' in thing2[i]:
            if len(outdata) < 951 and should_continue is True:
                can_continue = True
                pageToken = thing2[i]['nextPageToken']
        
    print can_continue
    print pageToken
    print should_continue
    print len(outdata)

csvoutfile = open('test-videos.csv','wb')
for key in outdata[0].iterkeys():
  fieldnames.append(key)
  print "wrote one"
writer = csv.DictWriter(csvoutfile,fieldnames)
writer.writeheader()
writer.writerows(outdata)
print "wrote stuff"
print channels
