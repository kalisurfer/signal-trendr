from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

# game scaffolding
gameCollection = db.games

games = gameCollection.find()

tags = set()

for game in games:
	genre = game.get("genre", [])
	if isinstance(genre, basestring):
		genre = [genre]
	for tag in genre:
		tags.add(tag)


for tag in tags:
	print tag
