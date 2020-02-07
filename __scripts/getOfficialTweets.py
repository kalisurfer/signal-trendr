# this file will start grabbing tweets from the weareplaying list on twitter

import twitter
import pprint
import datetime
import string
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit

# game scaffolding
tweetCollection = db.tweet
pp = pprint.PrettyPrinter(indent=4)

config = [
	{"id": "51821ab0bd028659d3bdf6d1", "name": "The Last of Us", "account":"tlougame", "tags": ["thelastofus", "tlougame", "the last of us game"]},
	{"id": "51821ab0bd028659d3bdf6d2", "name": "The Elder Scrolls Online", "account":"tesonline", "tags": ["@tesonline", "elderscrollsonline", "elder scrolls online"]},
	{"id": "51821ab0bd028659d3bdf6d3", "name": "Dust 514", "account":"ccp_dust514", "tags": ["dust514", "eve fps", "dust 514"]},
	{"id": "51821ab0bd028659d3bdf6d4", "name": "Beyond: Two Souls",  "account":"Beyond2SoulsPS3", "tags": ["beyondtwosouls", "beyond two souls", "@beyond_twosouls"]},
	{"id": "51821ab0bd028659d3bdf6d5", "name": "Grand Theft Auto V",  "account":"GTA5Updates", "tags": ["grandtheftautoV", "grand theft auto V", "GTAV", "GTA5"]},
	{"id": "51821ab0bd028659d3bdf6d6", "name": "Splinter Cell: Blacklist", "account":"SplinterCell", "tags": ["SplinterCellBlacklist", "Splinter Cell Blacklist", "@SplinterCell"]},
	{"id": "51821ab0bd028659d3bdf6d7", "name": "Deadpool", "account":"Deadpool", "tags": ["@realdeadpool", "deadpool"]},
	#{"id": "51821ab0bd028659d3bdf6d8", "name": "South Park: The Stick of Truth", "account":"tesonline", "tags": ["southparkstickoftruth", "south park stick of truth", "stickoftruth", "stick of truth"]},
	{"id": "51821ab0bd028659d3bdf6d9", "name": "Dota 2", "account":"DOTA2", "tags": ["dota2", "@dota2", "dota 2"]},
	{"id": "51821ab1bd028659d3bdf6da", "name": "Rainbow 6: Patriots", "account":"Rainbow6Game", "tags": ["rainbow 6 patriots", "rainbow6", "rainbow6patriots", "spies vs mercs", "rainbow 6"]},
	{"id": "51821ab1bd028659d3bdf6db", "name": "MechWarrior Online", "account":"mechwarriorf2p", "tags": ["@mechwarriorf2p", "mechwarriors", "mechwarrior f2p"]},
	#{"id": "51821ab1bd028659d3bdf6dc", "name": "Pikmin 3", "account":"tesonline", "tags": ["pikmin 3"]},
	{"id": "51821ab1bd028659d3bdf6dd", "name": "Total War: Rome II", "account":"TotalWarRome", "tags": ["totalwar"]},
	#{"id": "51821ab1bd028659d3bdf6de", "name": "Agent", "account":"tesonline", "tags": ["Agent video game"]},
	{"id": "51821ab1bd028659d3bdf6df", "name": "Animal Crossing: New Leaf", "account":"animalcrossing", "tags": ["Animal Crossing: New Leaf", "Animal Crossing New Leaf", "ACNL", "AnimalCrossingNewLeaf"]},
	{"id": "51821ab1bd028659d3bdf6e0", "name": "Metro: Last Light", "account":"MetroVideoGame", "tags": ["metrovideogame", "metro video game", "metro2013", "metrolastlight", "metro last light"]},
	{"id": "51821ab1bd028659d3bdf6e1", "name": "Arma III", "account":"Arma3official", "tags": ["armaIII", "arma III", "armaIIIofficial"]},
	{"id": "51821ab1bd028659d3bdf6e2", "name": "Final Fantasy XIV Online", "account":"FF_XIV_EN", "tags": ["Final Fantasy XIV", "FFIV", "FF_XIV_EN"]},
	{"id": "51821ab1bd028659d3bdf6e3", "name": "Lost Planet 3", "account":"LostPlanet", "tags": ["lost planet 3", "lostplanet3", "lostplanet"]},
	{"id": "51821ab2bd028659d3bdf6e4", "name": "Remember Me", "account":"remembermegame", "tags": ["remembermegame"]},
	{"id": "51821ab2bd028659d3bdf6e5", "name": "Battlefield 4", "account":"Battlefield", "tags": ["bf4", "bf 4", "battlefield4", "battlefield 4"]},
	{"id": "51821ab2bd028659d3bdf6e6", "name": "Call of Duty: Ghosts", "account":"callofduty", "tags": ["callofdutyghosts", "call of duty ghosts", "codghosts", "cod ghosts"]},
	{"id": "51821ab2bd028659d3bdf6e7", "name": "Watchdogs", "account":"Watchdogsgame", "tags": ["watch_dogs", "watch dogs", "#watchdogs"]},
	{"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "account":"assassinscreed", "tags": ["assassin's creed black flag", "acblackflag"]},
	#{"id": "51d7190ea0b7f98b6ed0cd8e", "name": "The Smurfs 2", "account":"tesonline", "tags": ["The Smurfs 2: The Video Game", "The Smurfs 2 The Video Game", "Smurfs 2 Video Game"]},
	#{"id": "51d7190ea0b7f98b6ed0cd90", "name": "Rise of the Triad", "account":"tesonline", "tags": ["Rise of the Triad", "ROTT2013"]},
	#{"id": "51d706d1e4b0a3dba82c201d", "name": "Limbo", "account":"tesonline", "tags": ["Limbo Video Game"]},
	#{"id": "51d70f6ee4b0a3dba82c2031", "name": "Monaco: What is Yours is Mine", "account":"tesonline", "tags": ["Monaco What is Yours is Mine"]},
	#{"id": "51d70fd2e4b0a3dba82c2034", "name": "Mortal Kombat", "account":"tesonline", "tags": ["Mortal Kombat"]},
	#{"id": "51d71001e4b0a3dba82c2035", "name": "Napoleon : Total War", "account":"tesonline", "tags": ["Napoleon Total War"]},
	#{"id": "51d71446a0b7f98b64f37419", "name": "Dark", "account":"tesonline", "tags": ["Dark Video Game"]},
	#{"id": "51d71446a0b7f98b64f3741a", "name": "Civilization V: Brave New World", "account":"tesonline", "tags": ["Civilization V Brave New World", "Civilization V"]},
	#{"id": "51d71446a0b7f98b64f3741b", "name": "Metal Gear Solid : The Legacy Collection", "account":"tesonline", "tags": ["Metal Gear Solid The Legacy Collection"]},
	{"id": "51d71446a0b7f98b64f3741c", "name": "NCAA Football 14", "account":"EANCAAFootball", "tags": ["NCAA Football 14", "NCAA14"]},
	#{"id": "51d71446a0b7f98b64f3741d", "name": "Toki Tori 2+", "account":"tesonline", "tags": ["Toki Tori 2"]},
	#{"id": "51d71446a0b7f98b64f3741e", "name": "Dynasty Warriors 8", "account":"tesonline", "tags": ["Dynasty Warriors 8"]},
	#{"id": "51d71446a0b7f98b64f3741f", "name": "Shin Megami Tensei IV", "account":"tesonline", "tags": ["Shin Megami Tensei IV", "Shin Megami Tensei 4"]},
	#{"id": "51d71446a0b7f98b64f37420", "name": "Time and Eternity", "account":"tesonline", "tags": ["Time and Eternity"]},
	#{"id": "51d71447a0b7f98b64f37421", "name": "Turbo: Super Stunt Squad", "account":"tesonline", "tags": ["Turbo: Super Stunt Squad", "Turbo Video Game"]},
	#{"id": "51d7190ea0b7f98b6ed0cd8f", "name": "Shadowrun Returns", "account":"tesonline", "tags": ["Shadowrun Returns"]},
	#{"id": "51d7190ea0b7f98b6ed0cd91", "name": "Ashes Cricket 2013", "account":"tesonline", "tags": ["AshesCricket2013","Ashes Cricket 2013 Video Game"]},
	#{"id": "51d7190fa0b7f98b6ed0cd92", "name": "Sir, You Are Being Hunted", "account":"tesonline", "tags": ["Sir You Are Being Hunted"]},
	#{"id": "51d7198aa0b7f98b6f99bfdd", "name": "Disney's Planes", "account":"tesonline", "tags": ["Disney's Planes Video Game"]},
	{"id": "51d7198aa0b7f98b6f99bfde", "name": "Dragon's Crown", "account":"DragonsCrown", "tags": ["Dragons Crown"]},
	#{"id": "51d7198ba0b7f98b6f99bfdf", "name": "Tales of Xillia", "account":"tesonline", "tags": ["Xillia"]},
	{"id": "51d7198ba0b7f98b6f99bfe0", "name": "Mario & Luigi: Dream Team", "account":"tesonline", "tags": ["Mario Luigi Dream Team", "MarioLuigiDreamTeam"]},
	#{"id": "51d71d58a0b7f98b77677744", "name": "Angry Birds Trilogy", "account":"tesonline", "tags": ["Angry Birds Trilogy", "AngryBirdsTrilogy"]},
	#{"id": "51d71d58a0b7f98b77677745", "name": "Europa Universalis IV", "account":"tesonline", "tags": ["Europa Universalis IV", "Europa Universalis 4", "EuropaUniversalisIV", "EuropaUniversalis4"]},
	#{"id": "51d71d58a0b7f98b77677746", "name": "Payday 2", "account":"tesonline", "tags": ["Payday 2", "Payday2"]},
	{"id": "51d71d58a0b7f98b77677747", "name": "Disney Infinity", "account":"tesonline", "tags": ["Disney Infinity", "InfinitePossibilities"]},
	{"id": "51d71d58a0b7f98b77677748", "name": "Saints Row IV", "account":"tesonline", "tags": ["Saints Row IV", "Saints Row 4", "SRIV"]},
	{"id": "51d71d58a0b7f98b77677749", "name": "The Bureau: XCOM Declassified", "account":"tesonline", "tags": ["XCOM Declassified"]},
	#{"id": "51d71d58a0b7f98b7767774a", "name": "Castlevania: Lords of Shadow", "account":"tesonline", "tags": ["Lords of Shadow"]},
	##{"id": "51d71d59a0b7f98b7767774b", "name": "Hatsune Miku: Project DIVA F", "account":"tesonline", "tags": ["Project DIVA F", "ProjectDIVAF"]},
	#{"id": "51d71d59a0b7f98b7767774c", "name": "Killer is Dead", "account":"tesonline", "tags": ["Killer is Dead Game"]},
	{"id": "51d71d59a0b7f98b7767774d", "name": "Madden NFL 25", "account":"EAMaddenNFL", "tags": ["Madden NFL 25", "Madden25"]},
	#{"id": "51d71d59a0b7f98b7767774e", "name": "War for the Overworld", "account":"tesonline", "tags": ["War for the Overworld"]},
	#{"id": "51d71d59a0b7f98b7767774f", "name": "Painkiller: Hell & Damnation", "account":"tesonline", "tags": ["Painkiller Hell & Damnation"]},
	#{"id": "51d71d59a0b7f98b77677750", "name": "SimCity", "account":"tesonline", "tags": ["SimCity Mac"]},
	{"id": "51d721f3a0b7f98b8d9ccafe", "name": "Diablo III", "account":"diablo", "tags": ["Diablo III Console"]},
	{"id": "51d721f3a0b7f98b8d9ccaff", "name": "Rayman Legends", "account":"RaymanGame", "tags": ["Rayman Legends", "RaymanLegends"]},
	{"id": "51d7223ba0b7f98b8f61332e", "name": "Killzone: Mercenary", "account":"killzone", "tags": ["Killzone Mercenary"]},
	{"id": "51d7223ba0b7f98b8f61332f", "name": "Kingdom Hearts HD 1.5 Remix", "account":"SquareEnix", "tags": ["Kingdom Hearts HD 1.5 Remix"]},
	{"id": "51d7223ba0b7f98b8f613330", "name": "NHL 14", "account":"EASPORTSNHL", "tags": ["NHL 14"]},
	#{"id": "51d7223ba0b7f98b8f613331", "name": "Puppeteer", "account":"tesonline", "tags": ["Puppeteer Game"]},
	{"id": "51d7223ba0b7f98b8f613332", "name": "Young Justice: Legacy", "account":"YoungJusticeVG", "tags": ["Young Justice Legacy", "YoungJustice"]},
	#{"id": "51d7223ba0b7f98b8f613333", "name": "The Wonderful 101", "account":"tesonline", "tags": ["Wonderful 101 Game"]},
	{"id": "51d7223ca0b7f98b8f613334", "name": "Broken Sword: The Serpent's Curse", "account":"revbot", "tags": ["Broken Sword The Serpent's Curse"]},
	{"id": "51d7223ca0b7f98b8f613335", "name": "Pro Evolution Soccer 2014", "account":"officialpes", "tags": ["Pro Evolution Soccer 2014", "PES2014"]},
	{"id": "51d7223ca0b7f98b8f613336", "name": "FIFA 14", "account":"EASPORTSFIFA", "tags": ["FIFA 14", "FIFA14"]},
	{"id": "51d7223ca0b7f98b8f613337", "name": "Deadfall Adventures", "account":"DeadfallAdv", "tags": ["Deadfall Adventures"]},
	{"id": "51d72298a0b7f98b9358ae52", "name": "Might & Magic X: Legacy", "account":"MightMagicGame", "tags": ["Might & Magic X: Legacy", "Might and Magic X: Legacy"]},
	#{"id": "51df5950e4b08a87384c3fb9", "name": "Injustice : Gods Among Us", "account":"tesonline", "tags": ["Injustice Gods Among Us"]},
	{"id": "51dfab57e4b0951818c02e33", "name": "Tom Clancy : The Division", "account":"TheDivisionGame", "tags": ["Tom Clancy The Division", "The Division Video Game"]},
	{"id": "520909d4e4b0fd1c4059f557", "name": "NBA 2K14", "account":"2KSports", "tags": ["NBA 2K14"]},
	#{"id": "52090d17e4b0fd1c4059f570", "name": "Etrian Odyssey Untold: The Millennium Girl", "account":"tesonline", "tags": ["Etrian Odyssey Untold The Millennium Girl"]},
	{"id": "5209833be4b056123d8a23fd", "name": "Pokemon X & Y", "account":"6thGenPokemon", "tags": ["Pokemon X Y"]},
	{"id": "5209689de4b0f243a315d711", "name": "Disgaea D2: A Brighter Darkness", "account":"NISAmerica", "tags": ["Disgaea D2"]},
	{"id": "5209666ae4b0f243a315d707", "name": "Just Dance 2014", "account":"justdancegame", "tags": ["JustDance2014"]},
	{"id": "5209c748e4b0f5e0f12b8c88", "name": "Skylanders: Swap Force", "account":"SkylandersGame", "tags": ["Skylanders Swap Force"]},
	#{"id": "5209c90de4b0f5e0f12b8c8a", "name": "Cabela's African Adventures", "account":"tesonline", "tags": ["Cabela's African Adventures"]},
	{"id": "5209525be4b0f243a315d668", "name": "NBA Live 14", "account":"EASPORTSNBA", "tags": ["NBA Live 14"]},
	{"id": "521fadc5e4b02c2d27ae597c", "name": "TitanFall", "account":"Titanfallgame", "tags": ["Titanfall"]},
	{"id": "5224fb6fe4b04c9630c4a3ff", "name": "Mighty No 9", "account":"MightyNo9", "tags": ["mightyno9"]},
	{"id": "52250be6e4b04c9630c4a43e", "name": "Planetary Annihilation", "account":"uberent",  "tags": ["Planetary Annihilation"]},
	{"id": "5225997fe4b06d1ef84aad5f", "name": "Dragon Age: Inquisition", "account": "dragonage", "tags": ["Dragon Age Inquisition", "#DAI"]},
	{"id": "52266052e4b05d0ae3b8312a", "name": "Star Citizen", "account": "RobertsSpaceInd", "tags": ["Star Citizen Game", "Star Citizen", "StarCitizen"]},
	{"id": "52266a0be4b05d0ae3b8315c", "name": "Torment: Tides of Numenera", "account": "BrianFargo", "tags": ["Torment Tides of Numenera", "Tides of Numenera"]},
	{"id": "5226b898e4b0a3867c4a4fac", "name": "XCOM: Enemy Within", "account": "XCOM", "tags": ["XCOM Enemy Within"]},
	{"id": "522bb86ce4b09d99b37f82ce", "name": "Need for Speed: Rivals", "account": "needforspeed", "tags": ["Need for Speed: Rivals", "nfsrivals"]},
	{"id": "522c1a40e4b09d99b37f8365", "name": "Ryse: Son of Rome", "account":"RyseSOR", "tags": ["Ryse: Son of Rome"]},
	{"id": "522c1ec5e4b09d99b37f8366", "name": "Dead Rising 3", "account" : "DeadRising", "tags": ["Dead Rising 3"]},
	{"id": "522c20f9e4b09d99b37f836c", "name": "Forza Motorsport 5", "account" : "ForzaMotorsport", "tags": ["Forza 5", "Forza Motorsport 5"]},
	{"id": "5237ff1ee4b08583f464bc1e", "name": "Project Spark", "account" : "proj_spark", "tags": ["Project Spark", "ProjectSpark"]},
	{"id": "5238024ae4b08583f464bc2a", "name": "Wolfenstein: The New Order", "account" : "wolfenstein", "tags": ["Wolfenstein: The New Order", "ProjectSpark"]},
	{"id": "523805a5e4b08583f464bc34", "name": "The Crew", "account" : "thecrewgame", "tags": ["The Crew Game", "thecrew"]},
	#{"id": "52394845e4b01f60c4e70f04", "name": "Crimson Dragon", "account" : "none", "tags": ["Crimson Dragon"]},
	{"id": "52394f95e4b01f60c4e70f28", "name": "The Fighter Within", "account" : "ubisoft", "tags": ["Figther Within Game"]},
	{"id": "52395684e4b01f60c4e70f32", "name": "Killer Instinct", "account" : "DoubleHelixGame", "tags": ["Killer Instinct Video Game", "#killerinstinct"]},
	{"id": "52395965e4b01f60c4e70f42", "name": "LocoCycle", "account" : "twisted_pixel", "tags": ["LocoCycle"]},
	{"id": "52395ac3e4b01f60c4e70f4c", "name": "Peggle 2", "account" : "popcap", "tags": ["Peggle 2"]},
	{"id": "52395cd6e4b01f60c4e70f55", "name": "Powerstar Golf", "account" : "zoemode", "tags": ["Powerstar Golf"]},
	{"id": "523a4beae4b086a29e2e4fae", "name": "Zoo Tycoon", "account" : "zoemode", "tags": ["Zoo Tycoon"]},
	{"id": "523a5664e4b086a29e2e4fca", "name": "Zumba Fitness: World Party", "account" : "zoemode", "tags": ["Zumba Fitness: World Party"]},
	{"id": "523a5832e4b086a29e2e4fd8", "name": "Infinity Blade III", "account" : "InfinityBlade", "tags": ["Infinity Blade III", "Infinity Blade 3"]},
	{"id": "523b4f12e4b0bfabc3ae1c7c", "name": "SoulCalibur: Lost Swords", "account" : "namcogames", "tags": ["SoulCalibur: Lost Swords", "Soul Calibur 2 HD", "Soul Calibur Lost Swords"]},
	{"id": "523fcc8ce4b0acbcc843303c", "name": "Awesomenauts: Starstorm", "account": "ronimogames", "tags": ["Awesomenauts: Starstorm", "Awesomenauts"]}, #kickstarter developer ronimop platformer moba arts
	{"id": "523fc60de4b0acbcc843302c", "name": "Trials: Frontier", "account": "RedLynxGamer", "tags": ["Trials: Frontier", "Trials Frontier"]}, 
	{"id": "524126efe4b06e71cbab75ac", "name": "Pocket Trains", "account": "nimblebits", "tags": ["Pocket Trains"]}, 
	{"id": "524143d6e4b0ec2eaa1de090", "name": "Fist of Awesome", "account": "nicollhunt", "tags": ["Fist of Awesome Game"]},
	{"id": "524294f4e4b05d554a37bdd5", "name": "Castlevania: Lords of Shadow 2", "account": "konami", "tags": ["Castlevania: Lords of Shadow 2"]}, #feb 2014 on PC PS3 XBOX 360 Konami Action 
	{"id": "52429cf1e4b05d554a37be13", "name": "Batman: Arkham Origins", "account": "BatmanArkham", "tags": ["Batman: Arkham Origins"]},
	{"id": "5243cdfae4b09673a26814ba", "name": "Shantae: Half-Genie Hero", "account": "WayForward", "tags": ["Shantae: Half-Genie Hero", "Shantae"]}, #WayForward / Wii U PS3 PS4 Vita Vita TV XBOX 360 XBOX One Steam PC
	{"id": "5243de63e4b09673a26814fb", "name": "Anomaly 2", "account": "11bitstudios", "tags": ["Anomaly 2 Game"]},
	{"id": "52467342e4b05d75effe73f1", "name": "Plant vs Zombies 2: It's About Time", "account": "plantsvszombies", "tags": []},
	{"id": "524677e7e4b05d75effe7402", "name": "Plant vs Zombies Garden Warfare", "account": "plantsvszombies", "tags": []}
	]

api = twitter.Api(
			consumer_key='BzfccKOYg0dqn05kFewHw',
			consumer_secret='y005oSkVM2k3CNN32GQxKk7YUJPOhA92Rj8Ij8tJnQ0',
			access_token_key='13264102-NMZFOKySbIqDwsPu5KVttcy2dNfmNb5uvyJu5GY',
			access_token_secret='tCLLpOsmbfzEpsjOkOnBlBKvMPJz1JPFc6DFBmknfTU')


#print "updating everything in the table to have a twittertype of 3"
#tweetCollection.update({},{"$set":{"tweettype":3}}, multi=True)
#print "done updating db"

# loop through the structure above
for c in config:
	print "seeking ", c.get("account")
	result = api.GetUserTimeline(screen_name=c.get("account"))
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
				"game": [game_id],
				"tweettype": 1
			}
		exisiting_tweet = tweetCollection.find_one({"_id": tweet.id})
		if exisiting_tweet:
			print("an existing tweet ", tweet.id)
			tweetCollection.update({"_id": tweet.id}, {"$set": {"tweettype": 1}})
				
		else:
			tweetCollection.save(post)
			print("tweet was inserted with ID ", tweet.id)
				


#listing = gameCollection.find({});

#http://cdn.superbwallpapers.com/wallpapers/games/call-of-duty-ghosts-19880-400x250.jpg

# set of arrays to get games in
# {"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "account":"tesonline", "tags": ["assassin's creed black flag", "acblackflag"]}
# gameCollection.update({}, { "$set": {"trendIndex": 0}}, upsert=False, multi=True)
#results = gameCollection.find({"releaseDate": { "$gt": datetime.datetime.utcnow() }});
#results = gameCollection.find({ "heroURL" : {"$not":{"$regex" : ".*localhost.*"}}});
#results = gameCollection.find({ "heroURL" : {"$regex" : ".*lorempixel.*"}});

#print dir(api)



	#print "the new date is "
	#print newDate
	#print "****** /n"