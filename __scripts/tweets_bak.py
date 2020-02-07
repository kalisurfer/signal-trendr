import twitter
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit
tweetCollection = db.tweet
gamesCollection = db.games

config = [
	{"id": "51821ab0bd028659d3bdf6d1", "name": "The Last of Us", "tags": ["thelastofus", "tlougame", "the last of us game"]},
	{"id": "51821ab0bd028659d3bdf6d2", "name": "The Elder Scrolls Online", "tags": ["@tesonline", "elderscrollsonline", "elder scrolls online"]},
	{"id": "51821ab0bd028659d3bdf6d3", "name": "Dust 514", "tags": ["dust514", "eve fps", "dust 514"]},
	{"id": "51821ab0bd028659d3bdf6d4", "name": "Beyond: Two Souls", "tags": ["beyondtwosouls", "beyond two souls", "@beyond_twosouls"]},
	{"id": "51821ab0bd028659d3bdf6d5", "name": "Grand Theft Auto V", "tags": ["grandtheftautoV", "grand theft auto V", "GTAV", "GTA5"]},
	{"id": "51821ab0bd028659d3bdf6d6", "name": "Splinter Cell: Blacklist", "tags": ["SplinterCellBlacklist", "Splinter Cell Blacklist", "@SplinterCell"]},
	{"id": "51821ab0bd028659d3bdf6d7", "name": "Deadpool", "tags": ["@realdeadpool", "deadpool"]},
	{"id": "51821ab0bd028659d3bdf6d8", "name": "South Park: The Stick of Truth", "tags": ["southparkstickoftruth", "south park stick of truth", "stickoftruth", "stick of truth"]},
	{"id": "51821ab0bd028659d3bdf6d9", "name": "Dota 2", "tags": ["dota2", "@dota2", "dota 2"]},
	{"id": "51821ab1bd028659d3bdf6da", "name": "Rainbow 6: Patriots", "tags": ["rainbow 6 patriots", "rainbow6", "rainbow6patriots", "spies vs mercs", "rainbow 6"]},
	{"id": "51821ab1bd028659d3bdf6db", "name": "MechWarrior Online", "tags": ["@mechwarriorf2p", "mechwarriors", "mechwarrior f2p"]},
	{"id": "51821ab1bd028659d3bdf6dc", "name": "Pikmin 3", "tags": ["pikmin 3"]},
	{"id": "51821ab1bd028659d3bdf6dd", "name": "Total War: Rome II", "tags": ["totalwar"]},
	{"id": "51821ab1bd028659d3bdf6de", "name": "Agent", "tags": ["Agent video game"]},
	{"id": "51821ab1bd028659d3bdf6df", "name": "Animal Crossing: New Leaf", "tags": ["Animal Crossing: New Leaf", "Animal Crossing New Leaf", "ACNL", "AnimalCrossingNewLeaf"]},
	{"id": "51821ab1bd028659d3bdf6e0", "name": "Metro: Last Light", "tags": ["metrovideogame", "metro video game", "metro2013", "metrolastlight", "metro last light"]},
	{"id": "51821ab1bd028659d3bdf6e1", "name": "Arma III", "tags": ["armaIII", "arma III", "armaIIIofficial"]},
	{"id": "51821ab1bd028659d3bdf6e2", "name": "Final Fantasy XIV Online", "tags": ["Final Fantasy XIV", "FFIV", "FF_XIV_EN"]},
	{"id": "51821ab1bd028659d3bdf6e3", "name": "Lost Planet 3", "tags": ["lost planet 3", "lostplanet3", "lostplanet"]},
	{"id": "51821ab2bd028659d3bdf6e4", "name": "Remember Me", "tags": ["remembermegame"]},
	{"id": "51821ab2bd028659d3bdf6e5", "name": "Battlefield 4", "tags": ["bf4", "bf 4", "battlefield4", "battlefield 4"]},
	{"id": "51821ab2bd028659d3bdf6e6", "name": "Call of Duty: Ghosts", "tags": ["callofdutyghosts", "call of duty ghosts", "codghosts", "cod ghosts"]},
	{"id": "51821ab2bd028659d3bdf6e7", "name": "Watchdogs", "tags": ["watch_dogs", "watch dogs", "#watchdogs"]},
	{"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "tags": ["assassin's creed black flag", "acblackflag"]},
	{"id": "51d7190ea0b7f98b6ed0cd8e", "name": "The Smurfs 2", "tags": ["The Smurfs 2: The Video Game", "The Smurfs 2 The Video Game", "Smurfs 2 Video Game"]},
	{"id": "51d7190ea0b7f98b6ed0cd90", "name": "Rise of the Triad", "tags": ["Rise of the Triad", "ROTT2013"]},
	{"id": "51d706d1e4b0a3dba82c201d", "name": "Limbo", "tags": ["Limbo Video Game"]},
	{"id": "51d70f6ee4b0a3dba82c2031", "name": "Monaco: What is Yours is Mine", "tags": ["Monaco What is Yours is Mine"]},
	{"id": "51d70fd2e4b0a3dba82c2034", "name": "Mortal Kombat", "tags": ["Mortal Kombat"]},
	{"id": "51d71001e4b0a3dba82c2035", "name": "Napoleon : Total War", "tags": ["Napoleon Total War"]},
	{"id": "51d71446a0b7f98b64f37419", "name": "Dark", "tags": ["Dark Video Game"]},
	{"id": "51d71446a0b7f98b64f3741a", "name": "Civilization V: Brave New World", "tags": ["Civilization V Brave New World", "Civilization V"]},
	{"id": "51d71446a0b7f98b64f3741b", "name": "Metal Gear Solid : The Legacy Collection", "tags": ["Metal Gear Solid The Legacy Collection"]},
	{"id": "51d71446a0b7f98b64f3741c", "name": "NCAA Football 14", "tags": ["NCAA Football 14", "NCAA14"]},
	{"id": "51d71446a0b7f98b64f3741d", "name": "Toki Tori 2+", "tags": ["Toki Tori 2"]},
	{"id": "51d71446a0b7f98b64f3741e", "name": "Dynasty Warriors 8", "tags": ["Dynasty Warriors 8"]},
	{"id": "51d71446a0b7f98b64f3741f", "name": "Shin Megami Tensei IV", "tags": ["Shin Megami Tensei IV", "Shin Megami Tensei 4"]},
	{"id": "51d71446a0b7f98b64f37420", "name": "Time and Eternity", "tags": ["Time and Eternity"]},
	{"id": "51d71447a0b7f98b64f37421", "name": "Turbo: Super Stunt Squad", "tags": ["Turbo: Super Stunt Squad", "Turbo Video Game"]},
	{"id": "51d7190ea0b7f98b6ed0cd8f", "name": "Shadowrun Returns", "tags": ["Shadowrun Returns"]},
	{"id": "51d7190ea0b7f98b6ed0cd91", "name": "Ashes Cricket 2013", "tags": ["AshesCricket2013","Ashes Cricket 2013 Video Game"]},
	{"id": "51d7190fa0b7f98b6ed0cd92", "name": "Sir, You Are Being Hunted", "tags": ["Sir You Are Being Hunted"]},
	{"id": "51d7198aa0b7f98b6f99bfdd", "name": "Disney's Planes", "tags": ["Disney's Planes Video Game"]},
	{"id": "51d7198aa0b7f98b6f99bfde", "name": "Dragon's Crown", "tags": ["Dragons Crown"]},
	{"id": "51d7198ba0b7f98b6f99bfdf", "name": "Tales of Xillia", "tags": ["Xillia"]},
	{"id": "51d7198ba0b7f98b6f99bfe0", "name": "Mario & Luigi: Dream Team", "tags": ["Mario Luigi Dream Team", "MarioLuigiDreamTeam"]},
	{"id": "51d71d58a0b7f98b77677744", "name": "Angry Birds Trilogy", "tags": ["Angry Birds Trilogy", "AngryBirdsTrilogy"]},
	{"id": "51d71d58a0b7f98b77677745", "name": "Europa Universalis IV", "tags": ["Europa Universalis IV", "Europa Universalis 4", "EuropaUniversalisIV", "EuropaUniversalis4"]},
	{"id": "51d71d58a0b7f98b77677746", "name": "Payday 2", "tags": ["Payday 2", "Payday2"]},
	{"id": "51d71d58a0b7f98b77677747", "name": "Disney Infinity", "tags": ["Disney Infinity", "InfinitePossibilities"]},
	{"id": "51d71d58a0b7f98b77677748", "name": "Saints Row IV", "tags": ["Saints Row IV", "Saints Row 4", "SRIV"]},
	{"id": "51d71d58a0b7f98b77677749", "name": "The Bureau: XCOM Declassified", "tags": ["XCOM Declassified"]},
	{"id": "51d71d58a0b7f98b7767774a", "name": "Castlevania: Lords of Shadow", "tags": ["Lords of Shadow"]},
	{"id": "51d71d59a0b7f98b7767774b", "name": "Hatsune Miku: Project DIVA F", "tags": ["Project DIVA F", "ProjectDIVAF"]},
	{"id": "51d71d59a0b7f98b7767774c", "name": "Killer is Dead", "tags": ["Killer is Dead Game"]},
	{"id": "51d71d59a0b7f98b7767774d", "name": "Madden NFL 25", "tags": ["Madden NFL 25", "Madden25"]},
	{"id": "51d71d59a0b7f98b7767774e", "name": "War for the Overworld", "tags": ["War for the Overworld"]},
	{"id": "51d71d59a0b7f98b7767774f", "name": "Painkiller: Hell & Damnation", "tags": ["Painkiller Hell & Damnation"]},
	{"id": "51d71d59a0b7f98b77677750", "name": "SimCity", "tags": ["SimCity Mac"]},
	{"id": "51d721f3a0b7f98b8d9ccafe", "name": "Diablo III", "tags": ["Diablo III Console"]},
	{"id": "51d721f3a0b7f98b8d9ccaff", "name": "Rayman Legends", "tags": ["Rayman Legends", "RaymanLegends"]},
	{"id": "51d7223ba0b7f98b8f61332e", "name": "Killzone: Mercenary", "tags": ["Killzone Mercenary"]},
	{"id": "51d7223ba0b7f98b8f61332f", "name": "Kingdom Hearts HD 1.5 Remix", "tags": ["Kingdom Hearts HD 1.5 Remix"]},
	{"id": "51d7223ba0b7f98b8f613330", "name": "NHL 14", "tags": ["NHL 14"]},
	{"id": "51d7223ba0b7f98b8f613331", "name": "Puppeteer", "tags": ["Puppeteer Game"]},
	{"id": "51d7223ba0b7f98b8f613332", "name": "Young Justice: Legacy", "tags": ["Young Justice Legacy", "YoungJustice"]},
	{"id": "51d7223ba0b7f98b8f613333", "name": "The Wonderful 101", "tags": ["Wonderful 101 Game"]},
	{"id": "51d7223ca0b7f98b8f613334", "name": "Broken Sword: The Serpent's Curse", "tags": ["Broken Sword The Serpent's Curse"]},
	{"id": "51d7223ca0b7f98b8f613335", "name": "Pro Evolution Soccer 2014", "tags": ["Pro Evolution Soccer 2014", "PES2014"]},
	{"id": "51d7223ca0b7f98b8f613336", "name": "FIFA 14", "tags": ["FIFA 14", "FIFA14"]},
	{"id": "51d7223ca0b7f98b8f613337", "name": "Deadfall Adventures", "tags": ["Deadfall Adventures"]},
	{"id": "51d72298a0b7f98b9358ae52", "name": "Might & Magic X: Legacy", "tags": ["Might & Magic X: Legacy", "Might and Magic X: Legacy"]},
	{"id": "51df5950e4b08a87384c3fb9", "name": "Injustice : Gods Among Us", "tags": ["Injustice Gods Among Us"]},
	{"id": "51dfab57e4b0951818c02e33", "name": "Tom Clancy : The Division", "tags": ["Tom Clancy The Division", "The Division Video Game"]},
	{"id": "520909d4e4b0fd1c4059f557", "name": "NBA 2K14", "tags": ["NBA 2K14"]},
	{"id": "52090d17e4b0fd1c4059f570", "name": "Etrian Odyssey Untold: The Millennium Girl", "tags": ["Etrian Odyssey Untold The Millennium Girl"]},
	{"id": "5209833be4b056123d8a23fd", "name": "Pokemon X & Y", "tags": ["Pokemon X Y"]},
	{"id": "5209689de4b0f243a315d711", "name": "Disgaea D2: A Brighter Darkness", "tags": ["Disgaea D2"]},
	{"id": "5209666ae4b0f243a315d707", "name": "Just Dance 2014", "tags": ["JustDance2014"]},
	{"id": "5209c748e4b0f5e0f12b8c88", "name": "Skylanders: Swap Force", "tags": ["Skylanders Swap Force"]},
	{"id": "5209c90de4b0f5e0f12b8c8a", "name": "Cabela's African Adventures", "tags": ["Cabela's African Adventures"]},
	{"id": "5209525be4b0f243a315d668", "name": "NBA Live 14", "tags": ["NBA Live 14"]},
	{"id": "520909d4e4b0fd1c4059f557", "name": "NBA 2K14", "tags": ["NBA 2K14"]}]


api = twitter.Api(
			consumer_key='BzfccKOYg0dqn05kFewHw',
			consumer_secret='y005oSkVM2k3CNN32GQxKk7YUJPOhA92Rj8Ij8tJnQ0',
			access_token_key='13264102-lYCsWuAaV2UfZ2VDhl2aqFd3TSTK7daL1kni3IPyT',
			access_token_secret='haTBm69Bw3pxZ8zvoSYtMZprOCO2694rXQEqxDQQ')


def parse_tweet_date(date):
	# TODO
	datetime.strptime(date, "")


def update_game(game_id, score):
	gamesCollection.update({"_id": ObjectId(game_id)}, {"$inc": {"trendIndex": score}})


for c in config:
	for tag in c.get("tags", []):
		lastID = tweetCollection.find({"game": c.get("id")}).sort("created_at", 1).limit(1)
		lastTweetID = lastID[0].get("_id")
		print lastID[0].get("text")
		#print lastID
		result = api.GetSearch(tag, count=100, include_entities=True, result_type="recent", since_id=lastTweetID)
		print c.get("name"), tag, len(result)
		game_id = c.get("id")
		for tweet in result:
			score = tweet.favorite_count + tweet.retweet_count + 1
			post = {
				"author": tweet.user.screen_name,
				"text": tweet.text,
				"_id": tweet.id,
				"authorID": tweet.user.id,
				"fav_count": tweet.favorite_count,
				"rt_count": tweet.retweet_count,
				"geo": tweet.geo,
				"created_at": tweet.created_at,
				"score": score,
				"game": [game_id]
			}
			exisiting_tweet = tweetCollection.find_one({"_id": tweet.id})
			if exisiting_tweet:
				print("an existing tweet ", tweet.id)
				if game_id not in exisiting_tweet.get("game", []):
					print "but gameID wasn't in"
					tweetCollection.update({"_id": tweet.id}, {"$addToSet": {"game": game_id}})
					update_game(game_id, score)
			else:
				tweetCollection.save(post)
				print("tweet was inserted with ID ", tweet.id)
				update_game(game_id, score)
