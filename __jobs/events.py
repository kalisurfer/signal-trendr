from datetime import datetime, timedelta
from collections import Counter
from numpy import array
from bson.objectid import ObjectId
from ingest import gamesCollection, gameHistory, db


descriptions = {
	"tijump": "Seriously Trending",
	"tibump": "Got a little boost",
	"tidrop": "Falling hard",
	"tidip": "Small dip",
	"rank1": "Reached #1",
	"rank5": "Broke the top 5",
	"rank10": "Broke the top 10",
	"rank1mobi": "Reached #1 for mobile",
	"rank5mobi": "Broke the top 5 for mobile",
	"rank10mobi": "Broke the top 10 for mobile",
	"rank1cf": "Reached #1 for crowdfunded",
	"rank5cf": "Broke the top 5 for crowdfunded",
	"rank10cf": "Broke the top 10 for crowdfunded",
}

class EventProcessor(object):
	"""
	rules to check for:
	[ ] entered top 10 for mobile (can not have been in last 2 weeks)
	[ ] entered top 10 for recent (can not have been in last 2 weeks)
	[ ] entered top 10 for crowdfunded (can not have been in last 2 weeks)
	[ ] entered top 5 for mobile (can not have been in last 2 weeks)
	[ ] entered top 5 for recent (can not have been in last 2 weeks)
	[ ] entered top 5 for crowdfunded (can not have been in last 2 weeks)
	[ ] became number 1 for mobile (can not have been in last 2 weeks)
	[ ] became number 1 for recent (can not have been in last 2 weeks)
	[ ] became number 1 for crowdfunded (can not have been in last 2 weeks)
	"""

	def __init__(self, now=None):
		self.db = db
		self.gameHistory = gameHistory
		self.set_now(now)

	def set_now(self, now):
		self.now = now
		if self.now is None:
			self.now = datetime.utcnow()
		self.now = self.now - timedelta(minutes=self.now.minute,
					seconds=self.now.second,
					microseconds=self.now.microsecond)
		self.history_limit = self.now - timedelta(days=14)

	def _all_games(self):
		games = gamesCollection.find(fields=["trendIndex", "_id", "title", "rank"]).sort("trendIndex", -1)
		return [game for game in games]

	def _load_history(self, game):
		history = self.gameHistory.find({"game": game.get("_id"), "dateAdded": {"$gte": self.history_limit, "$lt": self.now}}).sort("dateAdded", -1)
		snaps = [interval for interval in history]
		events = self.db.event.find({"game": game.get("_id"), "dateAdded": {"$gte": self.history_limit, "$lt": self.now}})
		events = [event for event in events]
		return (snaps, events)

	def analyze_all_games(self):
		games = self._all_games()
		for game in games:
			self.analyze_game(game)

	def create_event(self, type, game):
		description = descriptions[type] if type in descriptions.keys() else "Unknown Event"
		print game, self.now, description
		self.db.event.insert({"dateAdded": self.now, "type": type, "description": description, "game": ObjectId(game)})

	def analyze_game(self, game):
		history, events = self._load_history(game)
		if len(history):
			current = history[0].get("recent_rank", 0)
			if current > 0:
				self.anomalize_game(game, history, events)
				ranks = []
				for interval in history:
					ranks.append(interval.get("recent_rank", 0))
				while 0 in ranks:
					ranks.remove(0)
				counts = Counter(ranks)
				if len(ranks):
					if current == 1:
						if counts[1] == 1:
							self.create_event("rank1", game.get("_id"))
					elif current <=5:
						if not self.has_less(5, counts, current):
							self.create_event("rank5", game.get("_id"))
					elif current <=10:
						if not self.has_less(10, counts, current):
							self.create_event("rank10", game.get("_id"))

	def anomalize_game(self, game, history, events):
		if len(history) > 6:
			# calculate previous data
			p_data = history[1:5]
			p_data = [x.get("trendIndex") for x in p_data]
			p_div = array(p_data).std()
			data = [x.get("trendIndex") for x in history[:4]]
			arrayed = array(data)
			std = arrayed.std()
			rising = 0
			falling = 0
			p_rank = p_data[0]
			rank = data[0]
			if p_div:
				# rising action
				rising = (std - p_div) / p_div
			if p_rank > rank:
				# falling action
				falling = ((p_rank - rank) / (p_rank * 1.0)) * 100
			if rising > 30:
				self.create_event("tijump", game.get("_id"))
			elif rising > 10:
				self.create_event("tibump", game.get("_id"))
			if falling > 30:
				self.create_event("tidrop", game.get("_id"))
			elif falling > 20:
				self.create_event("tidip", game.get("_id"))

	def has_less(self, limit, counter, current):
		if counter[current] > 1:
			return True
		for index in counter.keys():
			if index != current and index <= limit:
				return True
		return False

