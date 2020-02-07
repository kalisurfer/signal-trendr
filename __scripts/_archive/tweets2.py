import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit
tweetCollection = db.tweet

#import MySQLdb
i = 0
# words = ["lost planet, lostplanet, #lostplanet3, @lostplanet"]
words = ["thelastofus, @tlougame, the last of us, @tesonline, elderscrollsonline, elder scrolls online, dust514, eve fps, dust 514, beyondtwosouls, beyond two souls, @beyond_twosouls, grandtheftautoV, grand theft auto V, GTAV, GTA5, SplinterCellBlacklist, Splinter Cell Blacklist, @SplinterCell, @realdeadpool, deadpool, southparkstickoftruth, south park stick of truth, stickoftruth, stick of truth, dota2, @dota2, dota 2, rainbow 6 patriots, rainbow6, rainbow6patriots, spies vs mercs, rainbow 6, @mechwarriorf2p, mechwarriors, mechwarrior f2p, totalwar, metrovideogame, metro video game, metro2013, metrolastlight, metro last light, armaIII, arma III, armaIIIofficial, lost planet 3, lostplanet3, lostplanet, remembermegame, bf4, bf 4, battlefield4, battlefield 4, callofdutyghosts, call of duty ghosts, codghosts, cod ghosts, watchdogs, assassin's creed black flag, acblackflag"]

#oauth with twitter
auth = tweepy.OAuthHandler('Tvx9ifISn70xG6g1SqscIg', 'XsqF2CkIfAFP4hJbZqJLYo2I9Bbwqhmqi6gJKOjaJMU')
auth.set_access_token('2677771-YO0S3tqHO5hJ57Cv5WudaCcC9A4WNCwVEJug9opok', 'aWJKX8Kh11dRXY1K7jgRIxaLazzEC6kOYQe2M0fhM4E')

#go out to twitter and get the words

#stream = tweepy.Stream(auth=auth, listener=YourListener())    
#stream.sample()
#print len(stream)

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    i = i + 1;
    def on_data(self, data):
    	if data.has_key("text"):
        	print data
        	#if tweet.has_key("text"):
        print i
       	#print data['text']
				#print "---" * 4 
        return True

    def on_error(self, status):
        print status


#go out to twitter and get the words

stream = Stream(auth=auth, listener=StdOutListener())
stream.filter(track=words)

