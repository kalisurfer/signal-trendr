
/*
 * GET List page.
 */

 /* this page is meant to handle the details from the index page and ideally also list out ranking of games by genres */
 
var inspect = require('sys').inspect;
var _s = require('underscore.string');
var async = require('async');
var filter = "trendIndex";
var ObjectId = require('mongodb').ObjectID;

exports.index = function(req, res) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		Historys = models.models.Historys,

		context = {title: 'We Are Playing It', data: [], details: [], user: req.user};

		//this is the fucked up way mongodb wants dynamic sorting criteria passed
		var ID = 1;
		var key = filter;
		var d = new Date(Date.now());
		var time = new Date()
		var days = -62;
		var cutoffD = time.setDate(time.getDate()+ days);
		var results;

		filter = "recent_rank";
		gameIds = [];
		kickIds = [];
		mobileIds = [];
		detailsData = [];
		detailsData2 = {};
		theDate = "";

		sorter = {};
		sorter[filter] = ID;
		

		//is there an index passed
		if (req.params.name) {
			//is this the main index?
			if (req.params.name == "main") {
				//set the page context
				context["rankingTitle"] = 'The most talked about games this hour';
				context["title"] = 'The most talked about games this hour'; 

				console.log("in main charts");
				Game.find({"releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort(sorter).exec(function (err, docs) {
					if(docs) {
						console.log("in data but back with data");
						context["data"] = docs;
						
						res.render('list', context);
					}
				});


				

			//Is this the kickstarter index
			} else if (req.params.name == "kickstarter") {
				context["rankingTitle"] = "Trending Kickstarter-Funded Games";
				context["title"] = "Trending Kickstarter-Funded Games";


				console.log("in kickstarter");
				Game.find({"genre": "Kickstarter","releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort(sorter).exec(function (err, docs) {
					if(docs) {
						console.log("in kick but back with data");
						context["data"] = docs;
						
						res.render('list', context);
					}
				});


			// is this the mobile index
			} else if (req.params.name == "mobile") {
				context["rankingTitle"] = "Trending Mobile Games";
				context["title"] = "Trending Mobile Games";
				
				console.log("in mobile");
				Game.find({"platform":{"$in": ["iOS", "Android", "PS Vita"]}, "releaseDate": {"$gt": cutoffD }, "recent_rank": {"$gt": 0}}).sort(sorter).exec(function (err, docs) {
					if(docs) {
						console.log("in mobile but back with data");
						context["data"] = docs;
						
						res.render('list', context);
					}
				});


			}

		} else {
			res.render('index', context);
		}
		
	

};

exports.list = require("./list").index;
