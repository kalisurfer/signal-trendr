import twitter
import re
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
	{"id": "51821ab0bd028659d3bdf6d5", "name": "Grand Theft Auto V", "tags": ["grandtheftautoV", "grand theft auto V", "GTAV", "GTA5", "GTA 5", "GTA V", "GTA", "Grand Theft Auto"]},
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
	{"id": "51821ab1bd028659d3bdf6e2", "name": "Final Fantasy XIV Online", "tags": ["Final Fantasy XIV", "FFIV", "FF_XIV_EN", "Final Fantasy XIV"]},
	{"id": "51821ab1bd028659d3bdf6e3", "name": "Lost Planet 3", "tags": ["lost planet 3", "lostplanet3", "lostplanet"]},
	{"id": "51821ab2bd028659d3bdf6e4", "name": "Remember Me", "tags": ["remembermegame"]},
	{"id": "51821ab2bd028659d3bdf6e5", "name": "Battlefield 4", "tags": ["bf4", "bf 4", "battlefield4", "battlefield 4"]},
	{"id": "51821ab2bd028659d3bdf6e6", "name": "Call of Duty: Ghosts", "tags": ["callofdutyghosts", "call of duty ghosts", "codghosts", "cod ghosts", "call of duty: ghost"]},
	{"id": "51821ab2bd028659d3bdf6e7", "name": "Watchdogs", "tags": ["watch_dogs", "watch dogs", "#watchdogs"]},
	{"id": "51821ab2bd028659d3bdf6e8", "name": "Assassin's Creed: Black Flag", "tags": ["assassin's creed black flag", "acblackflag", "creed IV","assassin's creed"]},
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
	{"id": "52090d17e4b0fd1c4059f570", "name": "Etrian Odyssey Untold: The Millennium Girl", "tags": ["Etrian Odyssey Untold The Millennium Girl", "Etrian Odyssey"]},
	{"id": "5209833be4b056123d8a23fd", "name": "Pokemon X & Y", "tags": ["Pokemon X Y", "Pokemon X", "Pokemon Y"]},
	{"id": "5209689de4b0f243a315d711", "name": "Disgaea D2: A Brighter Darkness", "tags": ["Disgaea D2"]},
	{"id": "5209666ae4b0f243a315d707", "name": "Just Dance 2014", "tags": ["JustDance2014"]},
	{"id": "5209c748e4b0f5e0f12b8c88", "name": "Skylanders: Swap Force", "tags": ["Skylanders Swap Force"]},
	{"id": "5209c90de4b0f5e0f12b8c8a", "name": "Cabela's African Adventures", "tags": ["Cabela's African Adventures"]},
	{"id": "5209525be4b0f243a315d668", "name": "NBA Live 14", "tags": ["NBA Live 14"]},
	{"id": "520909d4e4b0fd1c4059f557", "name": "NBA 2K14", "tags": ["NBA 2K14"]},
	{"id": "521fadc5e4b02c2d27ae597c", "name": "TitanFall", "tags": ["Titanfall"]},
	{"id": "5224fb6fe4b04c9630c4a3ff", "name": "Mighty No 9", "tags": ["mightyno9", "mighty no. 9", "mega man successor"]},
	{"id": "52250be6e4b04c9630c4a43e", "name": "Planetary Annihilation", "tags": ["Planetary Annihilation"]},
	{"id": "5225997fe4b06d1ef84aad5f", "name": "Dragon Age: Inquisition", "account": "dragonage", "tags": ["Dragon Age Inquisition", "Dragon Age III", "Dragon Age: Inquisition", "#DAI"]},
	{"id": "52266052e4b05d0ae3b8312a", "name": "Star Citizen", "account": "RobertsSpaceInd", "tags": ["Star Citizen Game", "Star Citizen", "StarCitizen"]},
	{"id": "52266a0be4b05d0ae3b8315c", "name": "Torment: Tides of Numenera", "account": "BrianFargo", "tags": ["Torment Tides of Numenera", "Tides of Numenera"]},
	{"id": "5226b898e4b0a3867c4a4fac", "name": "XCOM: Enemy Within", "account": "XCOM", "tags": ["XCOM Enemy Within", "XCOM", "XCOM: Enemy Within"]},
	{"id": "522bb86ce4b09d99b37f82ce", "name": "Need for Speed: Rivals", "account": "needforspeed", "tags": ["Need for Speed: Rivals", "nfsrivals"]},
	{"id": "522c1a40e4b09d99b37f8365", "name": "Ryse: Son of Rome", "account":"RyseSOR", "tags": ["Ryse: Son of Rome"]},
	{"id": "522c1ec5e4b09d99b37f8366", "name": "Dead Rising 3", "account" : "DeadRising", "tags": ["Dead Rising 3"]},
	{"id": "522c20f9e4b09d99b37f836c", "name": "Forza Motorsport 5", "account" : "ForzaMotorsport", "tags": ["Forza 5", "Forza Motorsport 5"]},
	{"id": "5237ff1ee4b08583f464bc1e", "name": "Project Spark", "account" : "proj_spark", "tags": ["Project Spark", "ProjectSpark"]},
	{"id": "5238024ae4b08583f464bc2a", "name": "Wolfenstein: The New Order", "account" : "wolfenstein", "tags": ["Wolfenstein: The New Order", "ProjectSpark"]},
	{"id": "523805a5e4b08583f464bc34", "name": "The Crew", "account" : "thecrewgame", "tags": ["The Crew Game", "thecrew"]},
	{"id": "52394845e4b01f60c4e70f04", "name": "Crimson Dragon", "account" : "none", "tags": ["Crimson Dragon"]},
	{"id": "52394f95e4b01f60c4e70f28", "name": "The Fighter Within", "account" : "ubisoft", "tags": ["Figther Within Game"]},
	{"id": "52395684e4b01f60c4e70f32", "name": "Killer Instinct", "account" : "DoubleHelixGame", "tags": ["Killer Instinct Video Game", "#killerinstinct"]},
	{"id": "52395965e4b01f60c4e70f42", "name": "LocoCycle", "account" : "twisted_pixel", "tags": ["LocoCycle"]},
	{"id": "52395ac3e4b01f60c4e70f4c", "name": "Peggle 2", "account" : "popcap", "tags": ["Peggle 2"]},
	{"id": "52395cd6e4b01f60c4e70f55", "name": "Powerstar Golf", "account" : "zoemode", "tags": ["Powerstar Golf"]},
	{"id": "523a4beae4b086a29e2e4fae", "name": "Zoo Tycoon", "account" : "zoemode", "tags": ["Zoo Tycoon"]},
	{"id": "523a5664e4b086a29e2e4fca", "name": "Zumba Fitness: World Party", "account" : "zoemode", "tags": ["Zumba Fitness: World Party"]},
	{"id": "523a5832e4b086a29e2e4fd8", "name": "Infinity Blade III", "account" : "InfinityBlade", "tags": ["Infinity Blade III", "Infinity Blade 3"]},
	{"id": "523b4f12e4b0bfabc3ae1c7c", "name": "SoulCalibur: Lost Swords", "account" : "namcogames", "tags": ["SoulCalibur: Lost Swords", "Soul Calibur 2 HD", "Soul Calibur Lost Swords"]},
	{"id": "523fcc8ce4b0acbcc843303c", "name": "Awesomenauts: Starstorm", "account": "ronimogames", "tags": ["Awesomenauts: Starstorm", "Awesomenauts"]}, 
	{"id": "523fc60de4b0acbcc843302c", "name": "Trials: Frontier", "account": "RedLynxGamer", "tags": ["Trials: Frontier", "Trials Frontier"]}, 
	{"id": "524126efe4b06e71cbab75ac", "name": "Pocket Trains", "account": "nimblebits", "tags": ["Pocket Trains"]}, 
	{"id": "524143d6e4b0ec2eaa1de090", "name": "Fist of Awesome", "account": "nicollhunt", "tags": ["Fist of Awesome Game"]},
	{"id": "524294f4e4b05d554a37bdd5", "name": "Castlevania: Lords of Shadow 2", "account": "konami", "tags": ["Castlevania: Lords of Shadow 2", "Castlevania"]}, #feb 2014 on PC PS3 XBOX 360 Konami Action 
	{"id": "52429cf1e4b05d554a37be13", "name": "Batman: Arkham Origins", "account": "BatmanArkham", "tags": ["Batman: Arkham Origins", "Batman", "Arkham Origins"]},
	{"id": "5243cdfae4b09673a26814ba", "name": "Shantae: Half-Genie Hero", "account": "WayForward", "tags": ["Shantae: Half-Genie Hero", "Shantae"]}, #WayForward / Wii U PS3 PS4 Vita Vita TV XBOX 360 XBOX One Steam PC
	{"id": "5243de63e4b09673a26814fb", "name": "Anomaly 2", "account": "11bitstudios", "tags": ["Anomaly 2 Game"]},
	{"id": "52467342e4b05d75effe73f1", "name": "Plant vs Zombies 2: It's About Time", "account": "plantsvszombies", "tags":""},
	{"id": "524677e7e4b05d75effe7402", "name": "Plant vs Zombies: Garden Warfare", "account": "plantsvszombies", "tags":""} #XBOX One XBOX 360 PC DEc 31 2014
	#{"id": "", "name":"", "account":"", "tags":["Metal Gear Solid V", "Metal Gear Solid"]} #
	]

# run through games and figure out matches to tweets whose gameID = 0


#results = tweetCollection.find({"$and": [{ "text" : {"$regex" : "final fantasy"}}, {"game": 0}]});
#results = tweetCollection.find({"$and": [{ "text" : re.compile("final fantasy", re.IGNORECASE)}, {"game": 0}]});
#if (results.count() > 0):
#	print("there was at least one match for ", results.count())
#	for d in results:
#		print("***********************")
#		print(d.get("text"))
#		print(d.get("author"))
#		print("***********************")
	

#	print("no matches for")

def update_game(game_id, score):
	gamesCollection.update({"_id": ObjectId(game_id)}, {"$inc": {"trendIndex": score}})

gamesSearch = gamesCollection.find({});

for c in gamesSearch:
	for tag in c.get("ed_tags", []):
		print("seeking matches for ", tag)
		results = tweetCollection.find({"$and": [{ "text" : re.compile(tag, re.IGNORECASE)}, {"game": 0}]});  
		if (results.count() > 0):
			print("there was", results.count(), " match for ", tag)
			for d in results:

				print("***********************")
				print(d.get("text"))
				print(d.get("author"))
				print("***********************")

			#	tweetCollection.update({"_id": d.get("_id")}, {"$set": {"game": c.get("id")}})
			#	update_game(c.get("id"), d.get("score"))
			#	print("updated DB")
			
		else:
			print("no matches for ", c.get("name"), "and the tag ", tag)





