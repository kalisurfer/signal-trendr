

var dataAccess = require('../lib/models'),
	ObjectID = require('mongodb').ObjectID,
	Game = dataAccess.models.Game,
	_ = require("underscore");

var tag_list = [
	
];


dataAccess.connect();


_.each(tag_list, function(tags) {
	Game.findOne({_id: tags.id}, function(err, game) {
		if(game) {
			try {
				game.ed_tags = tags.tags;
				game.save();
			} catch(e) {
				console.log("BROKE:",  tags.id, e);
			}
		}
	});
});

