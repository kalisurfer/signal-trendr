import tweepy
import MySQLdb
from tweepy.api import API
import json
#import time

class StreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        self.textlist = []
        self.userlist = []
        self.hashtags = []
        self.links = [] 
        self.db_connect = MySQLdb.connect (host = "HOSTNAME",
                                  user = "USER",
                                  passwd = "PASS",
                                  db = "TWEETS",
                                  charset = "utf8",
                                  use_unicode = True)
        self.api = api or API()
    
        self.cursor = self.db_connect.cursor()           
    
    def on_data(self, data):
        print data
        if 'in_reply_to_status_id' in data:
            print "found a status"
            print self.textlist.__len__()
            is_retweet = "false"
            tweet = json.loads(data)
            print type( tweet )
            if tweet.has_key("retweeted_status"):
                self.cursor.execute("""UPDATE Dethklok.tweet SET rts = rts+1 WHERE uid = %s""",(tweet["retweeted_status"]["user"]["id"]))
                self.db_connect.commit()
                is_retweet = "true"
            long1 = None
            lat1 = None
            if tweet["coordinates"] is not None:
                long1 = tweet["coordinates"][0]
                lat1 = tweet["coordinates"][1]
            
            self.textlist.append([tweet["id_str"],tweet["user"]["id"],tweet["in_reply_to_status_id"],tweet["text"],tweet["retweet_count"],long1,lat1,tweet["created_at"],is_retweet])
            self.userlist.append([tweet["user"]["id"],tweet["user"]["screen_name"],tweet["user"]["name"],tweet["user"]["statuses_count"],tweet["user"]["favourites_count"],tweet["user"]["description"],tweet["user"]["followers_count"],tweet["user"]["lang"],tweet["user"]["created_at"],tweet["user"]["followers_count"],tweet["user"]["statuses_count"],tweet["user"]["favourites_count"]])
            counter1 = 0
            h = [tweet["id_str"],'','','','']
            while len(tweet["entities"]["hashtags"]) > counter1 and counter1 < 4:
                h[counter1+1] = tweet["entities"]["hashtags"][counter1]["text"]
                counter1 += 1
            
            if len(tweet["entities"]["hashtags"]) > 1: self.hashtags.append(h)
            
            counter2 = 0
            l = [tweet["id_str"],'','','']
            while len(tweet["entities"]["urls"]) > counter2 and counter2 < 3:
                l[counter2+1]=tweet["entities"]["urls"][counter2]["expanded_url"]
                counter2 += 1
            
            if len(tweet["entities"]["urls"]) > 1: self.links.append(l)      
            
            if self.textlist.__len__() > 4 and self.userlist.__len__() > 4:
                self.cursor.executemany ("""INSERT INTO Dethklok.tweet (id,uid,reply_id,text,rts,longitude,latitude,date,sqldate,is_rt)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)""", (self.textlist))
                self.cursor.executemany ("""INSERT INTO Dethklok.users (uid,sname,uname,statuses,favourites,description,followers,lang,reg_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE followers = %s, statuses = %s,favourites = %s""", (self.userlist))
                self.db_connect.commit()
                self.userlist = []
                self.textlist = []
            
            if self.hashtags.__len__() > 4:
                self.cursor.executemany ("""INSERT INTO Dethklok.hashtags (tid,h1,h2,h3,h4)
                    VALUES (%s, %s, %s, %s, %s)""", (self.hashtags))
                self.db_connect.commit()
                self.hashtags = []
            
            if self.links.__len__() > 4:
                self.cursor.executemany ("""INSERT INTO Dethklok.links (tid,l1,l2,l3)
                    VALUES (%s, %s, %s, %s)""", (self.links))
                self.db_connect.commit()
                self.links = [] 
                
            print "made it to the end"
            return
        elif 'limit' in data:
            print "limited"
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return 
        elif 'delete' in data:
            print 'delete request'
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return 

    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        self.cursor.close()
        self.db_connect.close()
        return False
        
    def on_timeout(self):
        print 'timeout'
        if self.textlist.__len__() > 0 and self.userlist.__len__() > 0:
            self.cursor.executemany ("""INSERT INTO Dethklok.tweet (id,uid,reply_id,text,rts,longitude,latitude,date,sqldate,is_rt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)""", (self.textlist))
            self.cursor.executemany ("""INSERT INTO Dethklok.users (uid,sname,uname,statuses,favourites,description,followers,lang,reg_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE followers = %s, statuses = %s,favourites = %s""", (self.userlist))
            
        if self.hashtags.__len__() > 0:
            self.cursor.executemany ("""INSERT INTO Dethklok.hashtags (tid,h1,h2,h3,h4)
                VALUES (%d, %s, %s, %s, %s)""", (self.hashtags))

        if self.links.__len__() > 0:
            self.cursor.executemany ("""INSERT INTO Dethklok.links (tid,l1,l2,l3)
                VALUES (%d, %s, %s, %s)""", (self.links))
        self.db_connect.commit()
        self.textlist = []
        self.userlist = []
        self.hashtags = []
        self.links = [] 

def main():
             
    auth = tweepy.OAuthHandler("ASDF","ASDF")
    auth.set_access_token("ASDF", "ASDF")
    
    print "kicking it off"
    l = StreamListener()
    streamer = tweepy.Stream(auth=auth, listener=l)
    setTerms = ['dota2','ti3','roadtoti4','the international','dota 2']
    streamer.filter(track = setTerms)
    print "quitting?"
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'
