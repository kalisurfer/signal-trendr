
/*
 * A series of data feeds used to back charts and lists.
 */
var _ = require('underscore');
var ObjectId = require('mongodb').ObjectID;

exports.gameActivity = function(req, res) {
	var models = require("../lib/models"),
		Historys = models.models.Historys;

		if(req.params.gameid) {
			var fields = {"trendIndex": 1, "tp": 1};
			if(req.query.fields) {
				console.log(req.query.fields);
				fields = _.countBy(req.query.fields.split(","), function(f) {
					return f;
				});
			}
			console.log(fields);
			fields.dateAdded = 1;
			Historys.find({"game": ObjectId(req.params.gameid)}, fields).sort({dateAdded: -1}).limit(100).exec(function (err, docs) {
				res.send(JSON.stringify(docs));
			});
		} else {
			res.send(JSON.stringify({err: "no game id specified"}));
		}

};


