/*
 * GET details page.
 */
var inspect = require('sys').inspect;
var async = require('async');
var ObjectID = require('mongodb').ObjectID;

exports.index = function(req, res){

	console.log("-----------------------------------");
	console.log(req.params);
	console.log(req.params.id);

	var models = require("../lib/models"),
		Game = models.models.Game,
		Tweets = models.models.Tweet,
		User = models.models.User,
		Video = models.models.Videos,
		context = {title: 'weareplayingNOW', data: [], genre: [], trailers: [],  tweets: [], tracking: [], friends: [], user: req.user, trailersLib: []};

	//this pulls the last tweet
	//trying to pull latest tweet but things is erroring out
	// Me thinkg there should be a better way of pulling all those tweets besides making 3 query calls.

	async.parallel([

		// get official tweets
		function(callback) {
			console.log("in one");
			Tweets.find({"game": ObjectID(req.params.id), "tweettype": 1}).sort({"_id": -1}).limit(15).exec(function (err, docs) {
				if(docs) {
					console.log("in one but back with data");
					context["latest"] = docs;
					callback();
				}
			});
		},

		// get editorial tweets
		function(callback) {
			console.log("in two");
			Tweets.find({"game": ObjectID(req.params.id), "tweettype": 2}).sort({"_id": -1}).limit(12).exec(function (err, docs) {
				if(docs) {
					console.log("in two but back with data");
					context["editorial"] = docs;
					//console.log("TWEETSTWEETSTWEETSTWEETSTWEETSTWEETSTWEETS" + inspect(docs));
					callback();
				}
			});
		},

		// get fan tweets
		/*
		function(callback) {
			console.log("in three");
			Tweets.find({"game": ObjectID(req.params.id), "tweettype": 3}).sort({"_id": -1}).limit(12).exec(function (err, docs) {
				if(docs) {
					console.log("in three but back with data");
					context["tweets"] = docs;
					//console.log("TWEETSTWEETSTWEETSTWEETSTWEETSTWEETSTWEETS" + inspect(docs));
					callback();
				}
			});
		},
		*/

		// get user info if logged in
		function(callback) {
			console.log("in five");

			//check for loggedin user first
			if (req.user && req.user.twitterId) {
				//if user is logged in than check to see if this game is tracked
				console.log("running five with " + req.params.id + " and " + req.user.twitterId);
				User.find({"gamesTracked": ObjectID(req.params.id), "twitterId": req.user.twitterId}).exec(function (err, docs) {
					if(docs) {
						console.log("in tracking but back with data");
						//console.log(docs.getCount())
						console.log(inspect(docs));
						console.log("-------------");
						console.log(req.user.twitterId);
						context["tracking"] = docs;
						//console.log(docs[0].get('gamesTracked'))
						callback();
					} else {
						console.log("no docs");
						callback();
					}
				});
			} else {
				console.log("no twitterId");
				callback();
			}
		},

		// if user is logeed in figures out how many of their friends are tracking the game
		// check for friends
		/*
		function(callback) {
			console.log("running in six");

			//make sure user is logged in
			if (req.user && req.user.twitterId) {
				console.log("user is loggedin in six with " + req.params.id);
				//console.log("my friends are" + req.user.friends)

				User.find({"gamesTracked": ObjectID(req.params.id), "friends": req.user.twitterId}).exec(function (err, friend) {
					if (friend) {
						console.log("in friends and back with data")
						context["friends"] = friend	
						callback();
					} else {
						console.log(" no friend data")
						callback();
					}
				})
			} else {
				callback();
			}

		},*/


		// get trailers for game
		function(callback) {
			console.log ("calling trailers")

			Video.find({"game": ObjectID(req.params.id)}).sort({"publishedAt": -1}).exec(function(err, docs) {
				if (docs) {
					console.log("back with trailer data ")
					context["trailersLib"] = docs;
					callback();
				} else {
					console.log("no trailer data returned")
					callback();
				}
			})
		},

		// get game information
		function(callback) {
			console.log("in four");
			results = Game.find({"_id": ObjectID(req.params.id) }, function (err, docs) {;
			if (docs) {
				console.log("in four but back with data");
				genre = [docs[0].get('genre')];
				context["data"] = docs;
				context["genre"] = String(docs[0].get('genre')).split(",");
				context["trailers"] = String(docs[0].get('trailer')).split(",");
				//console.log("this is SWETTTTTTT" + inspect(context["trailers"]))
				callback();
			} else {
				callback();
			}
		});
	}],
	function(err, results) {
		console.log("in callback");
		if(req.headers['x-requested-with'] && req.headers['x-requested-with'] == "XMLHttpRequest") {
			if(context["data"].length > 0) {
				context["game"] = context["data"][0];
				delete context["data"];
			}
			//res.render('details', context);
			res.render('details-min', context);
			//res.send(JSON.stringify(context));
		} else {
			res.render('details', context);
		}
		
	});
	
	console.log("-----------------------------------");
};

exports.track = function(req, res) {
	console.log("-----------------------------------");

	var models = require("../lib/models"),
		redirectURL = "/details/" + req.params.id;
		User = models.models.User;

		console.log("trying with " + req.params.id + " and the user " + req.user.twitterId);

		req.user.gamesTracked.push(ObjectID(req.params.id));
		req.user.save(function(err){
			if (err) {
				console.log(err);
			}
		});
		console.log("updated table with id " + req.params.id + " and the user " + req.user.twitterId);

	//res.send(JSON.stringify({status: "OK"}))

	res.redirect(redirectURL);





	console.log("-----------------------------------");

};

exports.untrack = function(req, res) {
	console.log("-----------------------------------");

	var models = require("../lib/models"),
		/*redirectURL = "/details/" + req.params.id;*/
		redirectURL = "/home";
		User = models.models.User;
		var arrayPos = -1;

		console.log("trying to untrack with " + req.params.id + " and the user " + req.user.twitterId);
		arrayPos = req.user.gamesTracked.indexOf(req.params.id)
		console.log(" removing the item at " + arrayPos);

		if (arrayPos > -1) {
			req.user.gamesTracked.splice(arrayPos, 1)
		}

		req.user.save(function(err){
			if (err) {
				console.log(err);
			}
		});


		/*req.user.gamesTracked.push(ObjectID(req.params.id));
		req.user.save(function(err){
			if (err) {
				console.log(err);
			}
		});*/
		console.log("updated table with id " + req.params.id + " and the user " + req.user.twitterId);

	//res.send(JSON.stringify({status: "OK"}))

	res.redirect(redirectURL);





	console.log("-----------------------------------");

};







