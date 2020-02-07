
/*
 * GET home page.
 */
var inspect = require('sys').inspect;
var async = require('async');
var filter = "trendIndex";
var ObjectID = require('mongodb').ObjectID;

exports.index = function(req, res) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		User = models.models.User,
		Tweets = models.models.Tweet,
		Historys = models.models.Historys,
		data = [];
	var gamesTr = [];
	var	context = {title: 'weareplaying', data: [], tweets: [], rankings: [], user: req.user};
	var firstID = 0;
		context["rankingTitle"] = 'Games You Are Tracking';

		// user must be logged in

		// get games being tracked
		async.series([
			function(callback){
				results = User.findOne({"twitterId": req.user.twitterId}).exec( function(err, games) {

					if (err) { return callback(err); }
					if (!games || games.length === 0) {
						return callback(new Error('No games are being tracked'));
					}

					//set the local variable so others can useit
					gamesTr = games.gamesTracked;
					callback();
				});
			},

			// loop through the games tracked and grab the detail info
			
				function(callback) {
						gameinfo = Game.find({"_id": {"$in": gamesTr }}).exec(function(err, datas) {
							if(datas) {
								//console.log(JSON.stringify(datas));
								context["data"] = datas;
								console.log("The first game is ", datas[0]._id);
								firstID = datas[0]._id;
							}
							callback();
						});
				},


				//get the first trakced games tweets
				function(callback) {
					tweetinfo = Tweets.find({"game": firstID, "tweettype": 1}).sort({"_id": -1}).limit(15).exec(function(err, tweets) {
						if (tweets) {
							context["tweets"] = tweets;
						}
						callback();
					});
				},

				//get the last 5 rankings
				function(callback) {
					rankinfo = Historys.find({"game": firstID}).sort({"dateAdded": -1}).limit(5).exec(function(err, rankings) {
						if (rankings) {
							console.log("returned with rankings which are ", rankings);
							context["rankings"] = rankings;
						}
						callback();
					});
				},
			




		],
			function(err, results) {
				console.log("in callback");
				res.render('home', context);
			}

		);

/*
		results = User.findOne({"twitterId": req.user.twitterId}).exec(function(err, user) {
			if(user) {

				//
				

				
				//loop through gamesTracked and get information by query games db
				for (i=0; i < user.gamesTracked.length ; i++) {
					console.log("in loop " + i);
					console.log("the game id is " + user.gamesTracked[i]);

					if (i == 0){
						tweetinfo = Tweets.find({"game": user.gamesTracked[0], "tweettype": 1}).sort({"_id": -1}).limit(12).exec(function(err, data2) {
							if(data2) {
								//console.log(JSON.stringify(datas));
								console.log("pumping out tweets", i, " with this many records ", data2.length)
								context["tweets"] = data2;
							}
						});
					}

					gameinfo = Game.find({"_id": {"$in": user.gamesTracked }}).exec(function(err, datas) {
						if(datas) {
							//console.log(JSON.stringify(datas));
							context["data"] = datas;
							res.render('home', context);
						} else {
							res.render('home', context);
						}
					});
				}
			} else {
				res.render('home', context);
			}

			

		});

	*/	

};

exports.details = function(req, res) {
	console.log("-----------------------------------");
	console.log("in home details");
	console.log("-----------------------------------");
	var models = require("../lib/models"),
		Game = models.models.Game,
		User = models.models.User,
		Tweets = models.models.Tweet,
		Historys = models.models.Historys,
		data = [];
	var	context = {title: 'weareplaying', data: [], tweets: [], rankings: [], user: req.user};
		
			async.series([
				//GET game info
				function(callback){
					gameinfo = Game.find({"_id": ObjectID(req.params.id)}).exec(function(err, datas) {

						if (err) { return callback(err); }
						if (!datas || datas.length === 0) {
							return callback(new Error('No tweets are being tracked'));
						}

						//set the local variable so others can useit
						console.log("in data", datas)
						context["data"] = datas;
						callback();
					});
				},

				function(callback){
					results = Tweets.find({"game": ObjectID(req.params.id), "tweettype": 1}).sort({"_id": -1}).limit(15).exec( function(err, tweets) {

						if (err) { return callback(err); }
						if (!tweets || tweets.length === 0) {
							return callback(new Error('No tweets are being tracked'));
						}

						//set the local variable so others can useit
						console.log("in tweets", tweets)
						context["tweets"] = tweets;
						callback();
					});
				},

			//get the last 5 rankings
				function(callback) {
					console.log("going to get HISTORY");
					rankinfo = Historys.find({"game": ObjectID(req.params.id)}).sort({"dateAdded": -1}).limit(5).exec(function(err, rankings) {
						if (rankings) {
							console.log("returned with rankings which are ", rankings);
							context["rankings"] = rankings;
						}
						callback();
					});
				},
			],
			function(err, results) {
				console.log("in callback");
				res.render('details-min', context);
			})




			/*tweetinfo = Tweets.find({"game": ObjectID(req.params.id), "tweettype": 1}).sort({"_id": -1}).limit(12).exec(function(err, tweets) {
				if (tweets) {
					console.log("in tweets", tweets)
					context["tweets"] = tweets;
				}
				res.render('details-min', context);
			});*/



	console.log("-----------------------------------");

};
