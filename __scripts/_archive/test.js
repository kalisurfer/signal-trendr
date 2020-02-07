var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/trendr');

var ObjectId = mongoose.Schema.ObjectId;


var developerSchema = new mongoose.Schema({
		name: {type: String, unique: true},
	});

var publisherSchema = new mongoose.Schema({
		name: {type: String, unique: true},
	});

var platformSchema = new mongoose.Schema({
		name: {type: String, unique: true},
		generation: Number,
		dateAdded: {type: Date, default: Date.now},
	});

var gameSchema = new mongoose.Schema({
		title: {type: String, unique: true},
		heroUrl: String,
		thumbnailUrl: String,
		releaseDate: Date,
		dateAdded: {type: Date, default: Date.now},
		genre: String, //a game can have more than one genre
		platform: [platformSchema],
		developer: {type: ObjectId, ref: developerSchema},
		publisher: {type: ObjectId, ref: publisherSchema}
	});

//This is the raw repository for tweets.  Tweets contained it here are tweets returned by the streaming search service
var tweetSchema = new mongoose.Schema({
	_id: {type: Number, unique: true}
	text: String,
	tuID: Number,
	favCount: Number,
	rtCount: Number,
	date: Date,
	dateAdded: {type: Date, default: Date.now},
	})

var Developer = mongoose.model('Developer', developerSchema);
var Publisher = mongoose.model('Publisher', publisherSchema);
var Platform = mongoose.model('Platform', platformSchema);
var Game = mongoose.model('Game', gameSchema);
var Tweet = mongoose.model('Tweet', tweetSchema);


var ps3 = new Platform({name: "Playstation 3", generation: 3});
ps3.save();

console.log("saved a ps3");

mongoose.disconnect();


