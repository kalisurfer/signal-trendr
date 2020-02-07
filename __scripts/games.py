# this file will help create some of the basic framework needed to fill out the site

import tweetstream
import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

# game scaffolding
gameCollection = db.games

# set of arrays to get games in

t = ["Diablo III", "Rayman Legends", "Total War: Rome II", "Killzone: Mercenary", "Kingdom Hearts HD 1.5 Remix", "NHL 14", "Puppeteer", "Young Justice: Legacy", "The Wonderful 101", "Broken Sword: The Serpent's Curse", "Pro Evolution Soccer 2014", "FIFA 14", "Deadfall Adventures", "Might & Magic X: Legacy"]
picu = ["http://lorempixel.com/300/600/"]
thumbu = ["http://lorempixel.com/300/300/"]
rd = [datetime.date(2013,9,3), datetime.date(2013,9,3), datetime.date(2013,9,3), datetime.date(2013,9,10), datetime.date(2013,9,10), datetime.date(2013,9,10), datetime.date(2013,9,10), datetime.date(2013,9,10), datetime.date(2013,9,18), datetime.date(2013,9,20), datetime.date(2013,9,24), datetime.date(2013,9,27), datetime.date(2013,9,30) ]
mentions = 0
genre = ["Action", "Platform", "RTS", "FPS", "RPG", "Sports", "Platform", "RPG", "Action", "Adventure", "Sports", "Sports", "Adventure", "RPG"]


for i in range(len(t)):
	new_post = { 	"title": t[i],
					"heroURL": picu,
					"thumbUrl": thumbu,
					"releaseDate": str(rd[i]),
					"mentions": mentions * i,
					"genre": genre[i],
					"dateAdded": datetime.datetime.utcnow() }
	print new_post
	print "\n"
	print "-----" * 5

	insert_post = gameCollection.insert(new_post)
