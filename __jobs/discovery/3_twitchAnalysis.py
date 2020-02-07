'''
_discovery.3_twitchAnalysis -- grabs all games from twitch being streamed and notifies us of the games we are not tracking

'''

import sys
import requests


def get_games(offset):
	print "getting games from twitch"
	try:
		if offset:
			apiOffset = "".join("&offset=" + offset)
		else:
			apiOffset = ""

		apiRequest = "".join("https://api.twitch.tv/kraken/games/top?limit=100"+apiOffset)
		result = requests.get(apiRequest)

		return result.json()

	except Exception, e:
		print "there was an error"
    	return str(e)

stream_json = get_games(None)



if stream_json["_total"] > 0:
	for game in stream_json["top"]:
		print "Name", "  # of Viewers", "   # of Channels"
		print game["game"]["name"], game["viewers"], game["channels"]
		print game["game"]["giantbomb_id"]

#print stream_json