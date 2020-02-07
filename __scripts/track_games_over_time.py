import pymongo, csv
from bson.objectid import ObjectId
import datetime

client = pymongo.MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

#This is the genres to search, in case you want to make this a callable function
genres = ["FPS","Shooter"]

#The dates we're searching
start_time = datetime.datetime(2013, 12, 11)
end_time = datetime.datetime(2013,12,24)

#Just containers to use below
findtags = []
traffic_results = []
fieldnames = ["ID","Title","Max/Mean"]


for genre in genres:
	findtags.append({"genre":genre})

# game scaffolding
gameCollection = db.games
gameHist = db.game_history

games = gameCollection.find({"$or":findtags})

#generate an output header. CSV cruft, but also useful for axis labels
tempdate = start_time
while not(tempdate >= end_time):
	fieldnames.append(tempdate.isoformat())
	tempdate = tempdate + datetime.timedelta(days=1)
	
print fieldnames

#order is id, Title, Max/Mean, Value for each date
end_id = ObjectId.from_datetime(end_time)
start_id = ObjectId.from_datetime(start_time)

for game in games:
	print "----"
	print game.get("title")
	print game
	game_id = game.get("_id")
	game_title = game.get("title")
	thisgamemax = [game_id,game_title,"Max"]
	thisgamemean = [game_id,game_title,"Mean"]
	days = gameHist.find({"$and":[{"game":game_id},{"_id":{"$lte":end_id}},{"_id":{"$gte":start_id}}]}).sort("_id", pymongo.ASCENDING)
	
	tempdate2 = start_time
	for day in days:
		if day.get("_id") >= ObjectId.from_datetime(tempdate2):
			tempdate2 = tempdate2 + datetime.timedelta(days=1)
			print day.get("day_max")
			day_max = day.get("day_max")
			day_mean = day.get("day_mean")
			thisgamemax.append(day_max)
			thisgamemean.append(day_mean)
	print thisgamemax
	traffic_results.append(thisgamemax)
	traffic_results.append(thisgamemean)

#csv cruft. Replace if you want to push to a graphing service or another db
csvout = open("history_out.csv",'wb')
csvwriter = csv.writer(csvout)
csvwriter.writerow(fieldnames)
csvwriter.writerows(traffic_results)


#for tag in tags:
#	print tag