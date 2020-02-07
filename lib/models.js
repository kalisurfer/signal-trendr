var mongoose = require('mongoose');
var ObjectId = mongoose.Schema.ObjectId;


var gameSchema = new mongoose.Schema({
		title: {type: String, unique: true},
		description: String,
		heroUrl: String,
		thumbUrl: {type: String, default: 'http://placehold.it/210x270&text=BoxArt'},
		trendIndex: Number,
		releaseDate: Date,
		dateAdded: {type: Date, default: Date.now},
		platform: [String],
		trailer: [String],
		tags: [String],
		ed_tags: [String],
		cat_tags: [String],
		official: String,
		developer: String,
		publisher: String,
		theme: String
	});

//This is the raw repository for tweets.  Tweets contained it here are tweets returned by the streaming search service
var tweetSchema = new mongoose.Schema({
		_id: String,
		text: String,
		tuID: Number,
		favCount: Number,
		rtCount: Number,
		date: Date,
		dateAdded: {type: Date, default: Date.now},
	}, {"collection": "tweet"});


// User profile, uses twitter for login and profile data
var profileSchema = new mongoose.Schema({
		twitterId: {type: String, unique: true},
		username: String,
		photo: String,
		token: String,
		tokenSecret: String,
		friends: [Number],
		gamesTracked: [ObjectId],
		raw: mongoose.Schema.Types.Mixed
	}, {"collection": "profile"});

// this where game suggestions from the website are stored
var gameSuggestionsSchema = new mongoose.Schema({
	dateAdded: {type: Date, default: Date.now},
	title: String,
	email: String,
	inserted: Number
},
	{"collection": "game_suggestions"});

// this where game history is stored 
var historySchema = new mongoose.Schema({
	id: {type: String, unique: true},
	dateAdded: {type: Date, default: Date.now},
	trendIndex: Number,
	recent_rank: Number,
	shortTrend: Number,
	rank: Number,
	short_term_rank: Number,
	game: ObjectId,
	short_term_recent_rank: Number
},
	{"collection": "game_history"});

// this where events are stored
var eventSchema = new mongoose.Schema({
	dateAdded: {type: Date, default: Date.now},
	type: String,
	description: String,
	game: ObjectId
},
	{"collection": "event"});

var videoSchema = new mongoose.Schema({
	_id: {type: String, unique: true},
	publishedAt: {type: Date, default: Date.now},
	title: String,
	videoId: String,
	game: ObjectId
},
	{"collection": "video"});


// this is where users queue up for the release
var queueSchema = new mongoose.Schema({
	dateAdded: {type: Date, default: Date.now},
	email: String,
	referrer: String
},
	{"collection": "launch_queue"});

var Game = mongoose.model('Game', gameSchema);
var Tweet = mongoose.model('tweet', tweetSchema);
var User = mongoose.model('profile', profileSchema);
var Suggestions = mongoose.model('game_suggestions', gameSuggestionsSchema);
var Historys = mongoose.model('game_history', historySchema);
var Event = mongoose.model('event', eventSchema);
var Queue = mongoose.model('launch_queue', queueSchema);
var Videos = mongoose.model('video', videoSchema);

var options = {
  db: { native_parser: false },
  server: { poolSize: 5, keepAlive: 1 },
  user: 'trendr01',
  pass: 'letmeconnect'
};

var db_uri = 'mongodb://ds047988-a0.mongolab.com:47988/weareplayingit';

exports.connect = function() {
	mongoose.connect(db_uri, options);
};

exports.disconnect = function() {
	mongoose.disconnect();
};

exports.models = {
	Game: Game,
	Tweet: Tweet,
	User: User,
	Suggestions: Suggestions,
	Historys: Historys,
	Event: Event,
	Queue: Queue,
	Videos: Videos
};

exports.twitter_descriptions = {
		"Seriously Trending": " is seriously trending",
		"Got a little boost": " got a little boost",
        "Falling hard": " is falling hard",
        "Small dip": " took a small dip",
    	"Reached #1": " has reached the #1 spot",
        "Broke the top 5": " broke the top 5",
        "Broke the top 10": " broke the top 10",
        "Reached #1 for mobile": " reached #1 for mobile",
        "Broke the top 5 for mobile": " broke the top 5 for mobile",
        "Broke the top 10 for mobile": " broke the top 10 for mobile",
        "Reached #1 for crowdfunded": " reached the #1 spot for crowdfunded",
        "Broke the top 5 for crowdfunded": " broke the top 5 for crowdfunded",
        "Broke the top 10 for crowdfunded": " broke the top 10 for crowdfunded"
}


