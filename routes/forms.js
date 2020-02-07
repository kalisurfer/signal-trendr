
/*
 * POST FORM page.
 */

 /* This is meant to process the various user facing forms on the site */
 
var inspect = require('sys').inspect;
var filter = "trendIndex";
var ObjectID = require('mongodb').ObjectID;
var models = require("../lib/models"),
	Suggestions = models.models.Suggestions,
	Game = models.models.Game,
	Event = models.models.Event,
	Queue = models.models.Queue;


exports.suggestion = function(req, res) {
	console.log("-----------------------------------");
	console.log("in forms SUGGESTION ");
	console.log("-----------------------------------");

	var suggestion = new Suggestions({"title": req.body.game, "email": req.body.email, "inserted": 0});
	suggestion.save();

	//Suggestions.insert({"title": req.body.game, "email": req.body.email});

	console.log("with the following form fields ", req.body);
	console.log("-----------------------------------");

	res.redirect("/");

};

exports.events = function(req, res) {
	console.log("-----------------------------------");
	console.log("in EVENT NEW SUGGESTION ");
	console.log("-----------------------------------");

	var gameID = 0;

	console.log("looking for ", req.body.game);

	Game.find({"title": req.body.game}).limit(1).exec(function (err, docs) {
		if(docs.length > 0) {
			console.log("in data but back with data ", docs[0]._id);
			gameID = docs[0]._id;
			var newEvent = new Event({"description": req.body.event, "game": gameID, type: "user" });
			newEvent.save(function(err) {
				// we've updated the dog into the db here
				if (err) throw err;
				res.redirect("/admin/event");
			});
		} else {
			console.log("NO DATA");
		}
	});




	console.log("fields passed include ", req.body);
	

	console.log("-----------------------------------");
	

};

exports.game = function(req, res) {
	console.log("-----------------------------------");
	console.log("in CREATE NEW GAME ");
	console.log("-----------------------------------");

	var gameID = 0;

	console.log("looking for ", req.body.title);

	Game.find({"title": req.body.title}).limit(1).exec(function (err, docs) {
		if(docs.length > 0) {
			console.log("a game already exist", docs[0]._id);
			res.redirect("/admin/event");
		} else {
			console.log("that game does not exist so you are free to create your own");

			//set of new variables located to handle multiple answers
			newGenre = req.body.genre.split(",")
			newPlatform = req.body.platform.split(",")
			newTags = req.body.tags.split(",")
			newEdTags = req.body.edTags.split(",")

			console.log("this is the new genres being created ", newGenre)

			newGame = new Game({
				"title": req.body.title,
				"description": req.body.description,
				"dateAdded": new Date(),
				"releaseDate": req.body.releaseDate, //we will need to cast it to a date mongo can recognize
				"genre": newGenre,
				"platform": newPlatform,
				"tags": newTags,
				"ed_tags": newEdTags,
				"developer": req.body.developer,
				"publisher": req.body.publisher,
				"official": req.body.officialTwitter,
				"trailer": req.body.trailer
			})

			newGame.save(function(err) {
				// we've updated the dog into the db here
				console.log("saving a new game")
				if (err) throw err;
				res.redirect("/admin/game");
			});
		}
	});




	console.log("fields passed include ", req.body);
	

	console.log("-----------------------------------");
	

};

exports.queue = function(req, res) {
	console.log("-----------------------------------");
	console.log("in QUEUE NEW SIGNUP ");
	console.log("-----------------------------------");


	var newSignup = new Queue({
		"email": req.body.email
	});

	newSignup.save(function(err) {
				// we've updated the dog into the db here
				if (err) throw err;
				res.redirect("/launch/thankyou");
			});

	




	console.log("fields passed include ", req.body);
	

	console.log("-----------------------------------");
	

};

//exports.list = require("./list").index;
