
/*
 * GET home page.
 */
var inspect = require('sys').inspect;
var async = require('async');
var filter = "trendIndex";

exports.index = function(req, res) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		context = {title: 'We Are Playing It', data: [], kick: [], mobile: [], user: req.user};
		
		if (req.params.filterBy) {
			filter = req.params.filterBy;
		} else {
			context["rankingTitle"] = 'The most talked about games this hour';
			filter = "recent_rank";
			//filter = "shortTrend";
		}
		//this is the fucked up way mongodb wants dynamic sorting criteria passed
		var ID = 1;
		var key = filter;
		var d = new Date(Date.now());
		var time = new Date();
		var days = -62;
		var cutoffD = time.setDate(time.getDate()+ days);
		var results;

		sorter = {};

		sorter[filter] = ID;



		//var results = Game.find({}).sort({filter: -1}).exec(function (err, docs) {

		async.parallel([

			// get main charts
			function(callback) {
				console.log("in main charts");
				Game.find({"releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort(sorter).limit(5).exec(function (err, docs) {
					if(docs) {
						console.log("in data but back with data");
						context["data"] = docs;
						callback();
					}
				});
			},

			//get kickstarters
			function(callback) {
				console.log("in kickstarter");
				Game.find({"genre": "Kickstarter","releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort(sorter).limit(5).exec(function (err, docs) {
					if(docs) {
						console.log("in kick but back with data");
						context["kick"] = docs;
						callback();
					}
				});
			},

			//get mobile games
			function(callback) {
				console.log("in mobile");
				Game.find({"platform":{"$in": ["iOS", "Android", "PS Vita"]}, "releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort(sorter).limit(7).exec(function (err, docs) {
					if(docs) {
						console.log("in mobile but back with data");
						context["mobile"] = docs;
						callback();
					}
				});
			},


		],
		function(err, results) {
	 		console.log("in callback");
    		res.render('index', context);
		});


};
