
/*
 * GET Genre page.
 */

 /* this page is meant to handle the details from the index page and ideally also list out ranking of games by genres */
 
var inspect = require('sys').inspect;
var filter = "trendIndex";

exports.index = function(req, res) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		context = {title: 'We Are Playing It', data: [], user: req.user};

		//this is the fucked up way mongodb wants dynamic sorting criteria passed
		var ID = -1;
		var key = filter;
		var d = new Date(Date.now());
		var time = new Date()
		var days = -62;
		var cutoffD = time.setDate(time.getDate()+ days);
		var results;

		sorter = {};
		sorter[filter] = ID;
		

		//is there an index passed
		if (req.params.genre) {
			//is this the main index?

			context["rankingTitle"] = 'The most talked about '+ req.params.genre + '-genre games this week';
			context["title"] = 'The most talked about '+ req.params.genre + '-genre games this week'; 
			filter = "trendIndex";

			Game.find({"releaseDate": {"$gt": cutoffD }, "genre": req.params.genre }).sort(sorter).exec(function (err, docs) {
				if(docs) {
					console.log("in list data but back with data");
					context["data"] = docs;
				}
				res.render('genre', context);
			});
		}

			
		
	

};

exports.list = require("./genres").index;
