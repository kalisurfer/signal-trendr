from datetime import datetime, timedelta
from collections import Counter
from numpy import array
from bson.objectid import ObjectId
from ingest import gamesCollection, gameHistory, db
import json


def shakers(now):
	rack = {}
	current = gameHistory.find({"dateAdded": now, "recent_rank": {"$exists": 1}}).sort([("recent_rank", 1)])
	for time_slice in current:
		rack[str(time_slice.get("game"))] = {"current": time_slice.get("recent_rank")}
	last_hour = gameHistory.find({"dateAdded": now-timedelta(hours=1), "recent_rank": {"$exists": 1}}).sort([("recent_rank", 1)])
	for time_slice in last_hour:
		gid = str(time_slice.get("game"))
		if gid in rack.keys():
			rank = time_slice.get("recent_rank")
			rack[gid]["previous"] = rank
			rack[gid]["delta"] = rank - rack[gid]["current"]
			rack[gid]["delta_abs"] = abs(rack[gid]["delta"])
	
	counts = [(game.get("delta_abs"), key) for key, game in rack.iteritems()]
	counts.sort(key=lambda n: n[0], reverse=True)
	result = ["{0}\t{1}".format(*item) for item in counts]
	return "\r\n".join(result)

# now = datetime(2013, 11, 21, 18)
# shakers(now)
