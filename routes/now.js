
/*
 * GET home page.
 */
var inspect = require('sys').inspect;
var async = require('async');
var filter = "trendIndex";
var ObjectID = require('mongodb').ObjectID;
var _ = require('underscore');


function getSomeNowTweets(page, callback) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		Tweets = models.models.Tweet;
	var skip = (page * 50) - 50;
	console.log("loading some tweets");
	Tweets.find({"tweettype": 2}).sort({"_id": -1}).limit(75).skip(skip).exec(function(err, tweets) {
		if (tweets) {
			//console.log("got some tweets");
			if(page == 1) {
				//console.log("it's page one, we get tops too.");
				getTheTops(function(err, games) {
					if(games) {
						games["tweettype"] = "games";
						if(tweets.length > 3) {
							tweets.splice(2, 0, games);
						} else {
							tweets.splice(0, 0, games);
						}
					}
					//callback(null, {status: "ok", tweets: tweets});
				});

				getTheVideos(function(err, videos) {
					//console.log("get thevideos returned something")
					if(videos) {
						//console.log("WE HAVE VIDEOS AS IN ")
						//console.log(videos)
						videos["tweettype"] = "videos";
						if(tweets.length > 3) {
							tweets.splice(3, 0, videos);
						} else {
							tweets.splice(1, 0, videos);
						}
					}
					console.log("TWEETS")
					//console.log(tweets)
					callback(null, {status: "ok", tweets: tweets});
				});


			} else {
				callback(null, {status: "ok", tweets: tweets});
			}
		} else {
			callback({status: "error", err: err});
		}
	});
}


function getTheTops(callback) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		Tweets = models.models.Tweet;
	var d = new Date(Date.now());
	var time = new Date();
	var days = -62;
	var cutoffD = time.setDate(time.getDate()+ days);

	Game.find({"releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort("recent_rank").limit(5).exec(function (err, games) {
		if(games) {
			callback(null, {status: "ok", games: games});
		} else {
			callback({status: "error", err: err});
		}
	});
}

function getTheVideos(callback) {
	console.log("IN THE VIDEOS DUDE")
	var models = require("../lib/models"),
		Game = models.models.Game,
		Tweets = models.models.Tweet;
		Videos = models.models.Videos;
		
	var d = new Date(Date.now());
	var time = new Date();
	var days = -62;
	var cutoffD = time.setDate(time.getDate()+ days);

	Videos.find({}).sort({"publishedAt": -1}).limit(20).lean(true).exec(function (err, videos) {
		console.log("Number of videos is " + videos.length)

		if(!err) {
			callback(null, {status: "ok", videos: videos});
			/*console.log("VIDEOS VIDEOS VIDEOS " + videos)
			//console.log("THERE WERE NO ERRORS")
			var games = [], i=0;

			for(i=0;i<videos.length;i++) {
				//console.log("i = " + i)

				games.push(videos[i].game);
			}
			Game.find({_id: {"$in": games}}, {_id: 1, title: 1}).exec(function (err, videos) {
				//console.log("START START")


				var titles = {};
				_.each(games, function(game) {
					titles[game._id] = game.title;
				});
				_.each(videos, function(video) {
					var id = video.game;
					video.game = {title: titles[id], id: id};
				});
				//console.log("VIDEOS VIDEOS VIDEOS " + videos)
				callback(null, {status: "ok", videos: videos});
			});*/
		} else {
			callback({status: "error", err: err});
		}
	});
}


/*
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
*/


exports.index = function(req, res) {
	var	context = {title: 'weareplaying', data: [], tweets: [], editorial: [], user: req.user};
	console.log("Drawing the NOW Page")
	context["rankingTitle"] = 'Games You Are Tracking';
    res.render('now', context);

    // getSomeNowTweets(1, function(err, result) {
	//     context['tweets'] = result['tweets'];
	//     res.render('now', context);
	// });
};


exports.more = function(req, res) {
	var page = Number(req.params.page);
	getSomeNowTweets(page, function(err, result) {
			res.send(JSON.stringify(result));
		});
};


exports.clear = function(req, res) {
	res.writeHead(200, {'Content-Length': 22, 'Content-Type': 'image/png' });
	res.send('GIF89a\x01\x00\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00');
}
