var express = require("express"),
	ObjectID = require('mongodb').ObjectID,
	models = require('../../lib/models').models,
	twitter_descriptions = require('../../lib/models').twitter_descriptions,
	async = require('async'),
	_ = require('underscore');


function topMentionsNow(req, res) {
	models.Game.find(null, {_id: 1, title: 1, day_sum: 1, tp: 1}, {sort: {tp: -1}}).limit(10).exec(function(err, games) {
		if(!err) {
			res.send(JSON.stringify({games: games}));
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}

function topGames(req, res) {
	models.Game.find(null, {_id: 1, title: 1, day_sum: 1}, {sort: {day_sum: -1}}).limit(10).exec(function(err, games) {
		if(!err) {
			res.send(JSON.stringify({games: games}));
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}

function trendingGames(req, res) {
	models.Game.find({"recent_rank": {"$gt": 0}}, {_id: 1, title: 1, day_sum: 1, recent_rank: 1, delta_1_recent_rank: 1}, {sort: {delta_1_recent_rank: 1}}).limit(10).exec(function(err, trends) {
		if(!err) {
			res.send(JSON.stringify({games: trends}));
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}


function movers24(req, res) {
	models.Game.find({"recent_rank": {"$gt": 0}}, {_id: 1, title: 1, day_sum: 1, recent_rank: 1, delta_24_recent_rank: 1}, {sort: {delta_24_recent_rank: 1}}).exec(function(err, trends24) {
		if(!err) {
			res.send(JSON.stringify({games: trends24}));
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}


function mainRankings(req, res) {
	var time = new Date();
	var days = -62;
	var cutoffD = time.setDate(time.getDate()+ days);
	models.Game.find({"releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort({"recent_rank": 1}).limit(10).exec(function (err, games) {
		if(!err) {
			res.send(JSON.stringify({games: games}));
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}



function recentEvents(req, res) {
	models.Event.find({}).sort({"dateAdded": -1}).limit(20).lean(true).exec(function (err, events) {
		if(!err) {
			var games = [], i=0;
			for(i=0;i<events.length;i++) {
				games.push(events[i].game);
			}
			models.Game.find({_id: {"$in": games}}, {_id: 1, title: 1}).exec(function (err, games) {
				var titles = {};
				_.each(games, function(game) {
					titles[game._id] = game.title;
				});
				_.each(events, function(eventObj) {
					var id = eventObj.game;
					eventObj.game = {title: titles[id], id: id};
					eventObj.twitterdescription = twitter_descriptions[eventObj.description];
				});
				res.send(JSON.stringify({events: events}));
			});
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}


function recentVideos(req, res) {
	models.Videos.find({}).sort({"publishedAt": -1}).limit(20).lean(true).exec(function (err, videos) {
		if(!err) {
			var games = [], i=0;
			for(i=0;i<videos.length;i++) {
				games.push(videos[i].game);
			}
			models.Game.find({_id: {"$in": games}}, {_id: 1, title: 1}).exec(function (err, games) {
				var titles = {};
				_.each(games, function(game) {
					titles[game._id] = game.title;
				});
				_.each(videos, function(video) {
					var id = video.game;
					video.game = {title: titles[id], id: id};
				});
				res.send(JSON.stringify({videos: videos}));
			});
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}



function recentEditorials(req, res) {
	models.Tweet.find({"game": 0}, {_id: 1, text: 1, author: 1}, {sort: {created_at: -1}}).limit(15).exec(function(err, tweets) {
		if(!err) {
			res.send(JSON.stringify({tweets: tweets}));
		} else {
			res.send(JSON.stringify({err: err}));
		}
	});
}



function dashboardRoute(req, res) {
	res.render('admin/dashboard');
}

var ResponseCollector = function(id, callback) {
	return {
		send: function(data) {
				var pdata = JSON.parse(data);
				var response = {}
				response[id] = pdata;
				callback(null, response);
		}
	}
}

function allDashData(req, res) {
	async.parallel([
		function(callback) {
			topGames(null, ResponseCollector("top_games", callback));
		},
		function(callback) {
			topMentionsNow(null, ResponseCollector("top_mentions", callback));
		},
		function(callback) {
			trendingGames(null, ResponseCollector("trending", callback));
		}
	],
	function(err, results) {
		if(err) {
			res.send(JSON.stringify({err: err}));
		} else {
			var context = {};
			_.each(results, function(result) {
				_.each(result, function(value, key) {
					context[key] = value;
				})
			});
			res.send(JSON.stringify(context));
		}
	});
}


exports.addRoutes = function(applyUrl) {
	applyUrl('/dashboard', dashboardRoute);
	applyUrl('/dashboard/data', allDashData, true);
	applyUrl('/dashboard/data/games/top', topGames);
	applyUrl('/dashboard/data/games/mentions/top', topMentionsNow);
	applyUrl('/dashboard/data/games/trending', trendingGames);
	applyUrl('/dashboard/data/games/movers', movers24);
	applyUrl('/dashboard/data/list/main', mainRankings);
	applyUrl('/dashboard/data/events', recentEvents);
	applyUrl('/dashboard/data/videos', recentVideos);
	applyUrl('/dashboard/data/editorials', recentEditorials);
}


