var express = require("express");
var index = require('./');
var details = require('./details');
var admin = require('./admin');
var list = require('./list');
var genres = require('./genres');
var home = require('./home');
var about = require('./about');
var forms = require('./forms');
var launch = require('./launch');
var now = require('./now');
var data = require('./data');

//var basic = express.basicAuth('bipedal', '5@pians');

exports.applyUrls = function(app){
	admin.applyUrls('admin', app);
	app.get('/', /*basic,*/ now.index);
	app.get('/%7B%7B%20tweet.media_url%20%7D%7D', now.clear);
	app.get('/{{%20tweet.media_url%20}}', now.clear);
	app.get('/details/:id', /*basic,*/ details.index);
	app.get('/details/track/:id', /*basic,*/ details.track);
	app.get('/details/untrack/:id', /*basic,*/ details.untrack);
	app.get('/genres/:genre', /*basic,*/ genres.index);
	app.post('/forms/suggestion', /*basic,*/ forms.suggestion);
	app.post('/forms/newEvent', /*basic,*/ forms.events);
	app.post('/forms/newGame', /*basic,*/ forms.game);
	app.post('/forms/queue', forms.queue);
	app.get('/list/:name', /*basic,*/ list.index);
	app.get('/home', /*basic,*/ home.index);
	app.get('/home/details/:id', /*basic,*/ home.details);
	app.get('/about', /*basic,*/ about.index);
	app.get('/launch/thankyou', launch.thankyou);
	app.get('/launch', launch.index);
	app.get('/now', now.index);
	app.get('/now/:page', now.more);
	app.get('/game/history/:gameid', data.gameActivity);
};
