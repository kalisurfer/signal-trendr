import twitter
from pymongo import MongoClient
from bson.objectid import ObjectId
import re
import time
from datetime import datetime, timedelta
from collections import namedtuple
from numpy import array
from requests.exceptions import ConnectionError


client = MongoClient('mongodb://trendr01:letmeconnect@ds047988-a0.mongolab.com:47988/weareplayingit')
db = client.weareplayingit
tweetCollection = db.tweet
gamesCollection = db.games
gameHistory = db.game_history
days_60 = timedelta(days=60)
one_day = timedelta(hours=24)
one_hour = timedelta(hours=1)

TWITTER_KEY = 'MIzpe0HomjqE3AZ7sqzdTQ'
TWITTER_SECRET = '4AHlHwZVPeQ3GZG1RERd98KZQaV6pSRYc0980smH0'
TwitterUser = namedtuple('TwitterUser', ['id', 'token', 'tokenSecret'])


class TwitterWrapper(object):
	users = []

	def __init__(self):
		self._reset()

	def _reset(self):
		self.master_user = db.profile.find_one({'twitterId': 1865610738})
		profiles = db.profile.find({'twitterId': {"$ne": 1865610738}})
		for profile in profiles:
			if not profile.get("expired", False):
				self.users.append(TwitterUser(profile.get("twitterId"), profile.get("token"), profile.get("tokenSecret")))
		try:
			self.user = self.master_user
			self.api = twitter.Api(
				consumer_key=TWITTER_KEY,
				consumer_secret=TWITTER_SECRET,
				access_token_key=self.master_user.get("token"),
				access_token_secret=self.master_user.get("tokenSecret"))
		except twitter.TwitterError as e:
			code = e.message[0].get("code")
			if code == 88:
				print "getting throttled, pausing"
				time.sleep(30)
			elif code == 89:
				raise Exception("Master user has an expired token!!")

	def _new_user(self):
		try:
			if len(self.users) == 0:
				print "no more users, waiting and will reset."
				time.sleep(90)
				self._reset()
			self.user = self.users.pop(0)
			print "trying new user", self.user.id
			self.api = twitter.Api(
				consumer_key=TWITTER_KEY,
				consumer_secret=TWITTER_SECRET,
				access_token_key=self.user.token,
				access_token_secret=self.user.tokenSecret)
		except twitter.TwitterError as e:
			code = e.message[0].get("code")
			if code == 88:
				print "getting throttled, backing off for a bit."
				time.sleep(30)
			elif code == 89:
				print "expired token, updating user."
				db.profile.update({'twitterId': self.user.id}, {'$set': {'expired': True}})
				return self._new_user()
			else:
				print "unknown code:", code
				if len(self.users):
					print "have more users"
					return self._new_user()
				else:
					print "no more users, waiting and will reset."
					time.sleep(90)
					self._reset()

	def GetListTimeline(self, *args, **kwargs):
		try:
			return self.api.GetListTimeline(*args, **kwargs)
		except twitter.TwitterError as e:
			print "=" * 90
			print str(e)
			print "=" * 90
			self._new_user()
			return self.GetListTimeline(*args, **kwargs)

	def GetUserTimeline(self, *args, **kwargs):
		try:
			return self.api.GetUserTimeline(*args, **kwargs)
		except twitter.TwitterError as e:
			if hasattr(e.message[0], "get"):
				code = e.message[0].get("code")
			else:
				code = 0
				print "=" * 90
				print e.message[0]
				print "=" * 90
				# assume something bad happened and continue.
				return []
			if code == 34:
				print "=" * 90
				print str(e)
				print kwargs.get("screen_name"), "does not exist"
				print "=" * 90
				return []
			print "=" * 90
			print str(e)
			print "=" * 90
			self._new_user()
			return self.GetUserTimeline(*args, **kwargs)

	def GetSearch(self, *args, **kwargs):
		try:
			return self.api.GetSearch(*args, **kwargs)
		except twitter.TwitterError as e:
			print "=" * 90
			print str(e)
			print "=" * 90
			self._new_user()
			return self.GetSearch(*args, **kwargs)
		except ConnectionError as e:
			# rest for 4 seconds and try again.
			time.sleep(4)
			# this could be bad... if we have a bad url this could look forever.
			# generally I think these are twitter being weird or connection timeouts.
			return self.GetSearch(*args, **kwargs)



twitter_access = TwitterWrapper()


class Ingestion(object):
	
	def __init__(self, now=None):
		self.counts = {}
		if now:
			self.now = now
			print "processing games for", now
			games = self._all_games()
			self.counts = {str(game.get("_id")):0 for game in games}
			print "set counts"
			self.get_editorial_tweets()
			print "editorials loaded"
			for game in games:
				self.assign_editorials(game)
			print "editorials analyzed"
			print "loading all tweets"
			self.load_all(games)
			print "applying scores"
			self.apply_scores()
			print "degrading games"
			self.degrade_games()
			print "creating history points"
			self.snapshot_games()
			print "adding metrics"
			self.add_game_metrics()
			print "done"

	def apply_scores(self):
		relevant_tweets = tweetCollection.find({"created_at": {"$gte": self.now-one_hour, "$lt": self.now}}, fields=["game", "score"])
		for tweet in relevant_tweets:
			score = tweet.get("score", 0)
			games = tweet.get("game", [])
			for game in games:
				self._update_game(str(game), score)

	def _update_game(self, game_id, score):
		if game_id != 0:
			if game_id in self.counts.keys():
				self.counts[game_id] += score

	def _parse_tweet_date(self, dte):
		return datetime.strptime(dte, '%a %b %d %H:%M:%S +0000 %Y')

	def _store_tweet(self, game_id, tweet, type):
		if game_id != 0:
			game_id = ObjectId(game_id)
		score = self._score_tweet(tweet)
		post = {
			"author": tweet.user.screen_name,
			"text": tweet.text,
			"_id": str(tweet.id),
			"authorID": tweet.user.id,
			"fav_count": tweet.favorite_count,
			"rt_count": tweet.retweet_count,
			"geo": tweet.geo,
			"created_at": self._parse_tweet_date(tweet.created_at),
			"score": score,
			"game": [game_id],
			"urls": [{"url": url.url, "expanded_url": url.expanded_url} for url in tweet.urls],
			"media": [{"media_url": media.get("media_url"), "expanded_url": media.get("expanded_url"), "type": media.get("type"), "sizes": media.get("sizes")} for media in tweet.media],
			"hashtags": [tag.text for tag in tweet.hashtags],
			"tweettype": type
		}
		exisiting_tweet = tweetCollection.find_one({"_id": str(tweet.id)})
		if exisiting_tweet:
			print("an existing tweet ", tweet.id)
			if game_id not in exisiting_tweet.get("game", []) and game_id != 0:
				print "but gameID wasn't in"
				tweetCollection.update({"_id": tweet.id}, {"$addToSet": {"game": game_id}, "$set": {"tweettype": type}})
		else:
			tweetCollection.save(post)
			print("tweet was inserted with ID ", tweet.id)

	def _score_tweet(self, tweet):
		return tweet.favorite_count + tweet.retweet_count + 1

	def _degrade_score(self, game):
		score = game.get("trendIndex", 0)
		score *= 0.8
		gamesCollection.update({"_id": game.get("_id")}, {"$set": {"trendIndex": int(score)}})

	def snapshot_games(self):
		for game_id, count in self.counts.iteritems():
			print game_id, count
			gamesCollection.update({"_id": ObjectId(game_id)}, {"$inc": {"trendIndex": count}})
		histories = {}
		# I guess we include all games in the snapshots
		games = gamesCollection.find(fields=["_id", "rank", "trendIndex"]).sort("trendIndex", -1)
		print "games loaded", games.count()
		for game in games:
			histories[game.get("_id")] = {
				"game": game.get("_id"),
				"trendIndex": game.get("trendIndex"),
				"dateAdded": self.now,
				"tp": self.counts.get(str(game.get("_id"))),
			}

		self._snap_games("rank", {"trendIndex": {"$gt": 0}}, "trendIndex", histories)
		self._snap_games("recent_rank", {"trendIndex": {"$gt": 0}, "releaseDate": {"$gt": self.now - days_60}}, "trendIndex", histories)
		self._snap_games("mobi_rank", {"trendIndex": {"$gt": 0}, "releaseDate": {"$gt": self.now - days_60}, "platform": {"$in": ["iOS", "Android", "PS Vita"]}}, "trendIndex", histories)
		self._snap_games("cs_rank", {"trendIndex": {"$gt": 0}, "releaseDate": {"$gt": self.now - days_60}, "genre": "Kickstarter"}, "trendIndex", histories)
		
		for id, game in histories.iteritems():
			print id, game
			gameHistory.update({"game": game.get("game"), "dateAdded": self.now}, game, upsert=True)

	def _add_metrics(self, game_id):
		history = gameHistory.find({"game": game_id, "dateAdded": {"$lt": self.now, "$gt": self.now-one_day}}).sort([("dateAdded", -1,)])
		last_24_hours = [e for e in history]
		tps = [ent.get("tp") or 0 for ent in last_24_hours]
		std = 0
		mean = 0
		min = 0
		max = 0
		if len(tps) > 2:
			nums = array(tps)
			std = nums.std()
			mean = nums.mean()
			max = int(nums.max())
			min = int(nums.min())
		the_set = {
			"day_sum": sum(tps),
			"day_std": std,
			"day_mean": mean,
			"day_max": max,
			"day_min": min,
		}
		update = {
			"$set": the_set
		}
		gameHistory.update({"game": game_id, "dateAdded": self.now}, update)
		current = gameHistory.find_one({"game": game_id, "dateAdded": self.now})
		if current:
			the_set["rank"] = current.get("rank")
			the_set["recent_rank"] = current.get("recent_rank")
			the_set["mobi_rank"] = current.get("mobi_rank")
			the_set["cs_rank"] = current.get("cs_rank")
			update = {
				"$set": the_set
			}
			previous = gameHistory.find_one({"game": game_id, "dateAdded": self.now-one_hour})
			if previous:
				the_set["delta_1_rank"] = current.get("rank", 0) - previous.get("rank", 0)
				the_set["delta_1_recent_rank"] = current.get("recent_rank", 0) - previous.get("recent_rank", 0)
				the_set["delta_1_mobi_rank"] = current.get("mobi_rank", 0) - previous.get("mobi_rank", 0)
				the_set["delta_1_cs_rank"] = current.get("cs_rank", 0) - previous.get("cs_rank", 0)
			previous = gameHistory.find_one({"game": game_id, "dateAdded": self.now-timedelta(hours=4)})
			if previous:
				the_set["delta_4_rank"] = current.get("rank", 0) - previous.get("rank", 0)
				the_set["delta_4_recent_rank"] = current.get("recent_rank", 0) - previous.get("recent_rank", 0)
				the_set["delta_4_mobi_rank"] = current.get("mobi_rank", 0) - previous.get("mobi_rank", 0)
				the_set["delta_4_cs_rank"] = current.get("cs_rank", 0) - previous.get("cs_rank", 0)
			previous = gameHistory.find_one({"game": game_id, "dateAdded": self.now-timedelta(hours=24)})
			if previous:
				the_set["delta_24_rank"] = current.get("rank", 0) - previous.get("rank", 0)
				the_set["delta_24_recent_rank"] = current.get("recent_rank", 0) - previous.get("recent_rank", 0)
				the_set["delta_24_mobi_rank"] = current.get("mobi_rank", 0) - previous.get("mobi_rank", 0)
				the_set["delta_24_cs_rank"] = current.get("cs_rank", 0) - previous.get("cs_rank", 0)
		gamesCollection.update({"_id": game_id}, update)

	def add_game_metrics(self):
		games = gamesCollection.find(fields=["_id"])
		for game in games:
			self._add_metrics(game.get("_id"))

	def _snap_games(self, name, query, sort, histories):
		rank = 0
		games = gamesCollection.find(query, fields=["_id", "rank", "trendIndex"]).sort(sort, -1)
		for game in games:
			rank += 1
			histories[game.get("_id")][name] = rank

	def degrade_games(self):
		games = gamesCollection.find(fields=["_id", "rank", "trendIndex"]).sort("trendIndex", -1)
		for game in games:
			self._degrade_score(game)

	def get_editorial_tweets(self):
		print "----------------------------------------"
		print " get_editorial_tweets"
		print "----------------------------------------"
		lastID = tweetCollection.find({"game": 0}).sort("_id", -1).limit(1)
		if lastID.count():
			lastTweetID = lastID[0].get("_id")
			result = twitter_access.GetListTimeline(list_id=95200241, include_entities=True, slug="wrplaying-blogs", count=200, since_id=lastTweetID)
		else:
			result = twitter_access.GetListTimeline(list_id=95200241, include_entities=True, slug="wrplaying-blogs", count=200)
		for tweet in result:
			self._store_tweet(0, tweet, 2)
		print "----------------------------------------"

	def assign_editorials(self, game):
		game_id = game.get("_id")
		for tag in game.get("ed_tags", []):
			results = tweetCollection.find({ "text" : re.compile(tag, re.IGNORECASE), "game": 0})
			for d in results:
				tweetCollection.update({"_id": d.get("_id")}, {"$set": {"game": [game_id]}})

	def get_official(self, game):
		acct = game.get("official")
		game_id = game.get("_id")
		if acct:
			print "loading tweets for", game_id, acct
			result = twitter_access.GetUserTimeline(screen_name=acct, include_entities=True)
			for tweet in result:
				self._store_tweet(game_id, tweet, 1)
		else:
			print "no official account for", game_id

	def _all_games(self):
		games = gamesCollection.find(fields=["tags", "_id", "title", "trendIndex", "official", "ed_tags"])
		return [game for game in games]

	def load_all(self, games):
		for game in games:
			self.get_official(game)
			self.load_tweets(game)

	def load_tweets(self, game):
		lastID = tweetCollection.find({"game": game.get("_id")}).sort("_id", -1).limit(1)
		if lastID.count():
			lastTweetID = lastID[0].get("_id")
		else:
			lastTweetID = None
		for tag in game.get("tags", []):
			if lastTweetID:
				result = twitter_access.GetSearch(tag, count=100, include_entities=True, result_type="recent", since_id=lastTweetID)
			else:
				result = twitter_access.GetSearch(tag, count=100, include_entities=True, result_type="recent")
			print game.get("_id"), tag, len(result)
			# if the len is 100 we should recurse with the max_id set to the lowest id number in the set. TODO
			game_id = game.get("_id")
			for tweet in result:
				self._store_tweet(game_id, tweet, 3)
