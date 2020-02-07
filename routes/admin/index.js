var express = require("express"),
	ObjectID = require('mongodb').ObjectID,
	models = require('../../lib/models').models;
	async = require('async'),
	dashboard = require('./dashboard');


function index(req, res) {
	models.Game.find(null, {_id: 1, title: 1}, {sort: {title: 1}}).exec(function(err, games) {
		res.render('admin/index', {games: games});
	});
}


function gameForm(req, res) {
	models.Game.find(null, {_id: 1, title: 1}, {sort: {title: 1}}).exec(function(err, games) {
		res.render('admin/game', {games: games});
	});
}

function gameDetail(req, res) {
	try {
		var id = ObjectID(req.params["id"]);
	} catch(e) {
		res.render('admin/index', {games: games});
	}
	models.Game.find(null, {_id: 1, title: 1}, {sort: {title: 1}}).exec(function(err, games) {
		res.render('admin/index', {games: games});
	});
}

function gameEvent(req, res) {
	models.Game.find(null, {_id: 1, title: 1}, {sort: {title: 1}}).exec(function(err, games) {
		res.render('admin/event', {games: games});
	});
}
function newEvent(req, res) {
	console.log("-----------------------------------");
	console.log("in ADMIN EVENT NEW SUGGESTION ");
	console.log("-----------------------------------");

	console.log("fields passed include ", req.body);
	

	console.log("-----------------------------------");
}


exports.applyUrls = function(prefix, app){
	console.log("applying admin urls");
	if(prefix.charAt(0) != '/') {
		prefix = '/' + prefix;
	}
	// drop the basic auth middleware in all these.  once we remove it from the top this will work and admin will be "secure".
	function applyUrl(path, handler, bypass) {
		if(bypass) {
			app.get(prefix + path, handler);
		} else {
			app.get(prefix + path, express.basicAuth('bipedal', '5@pians'), handler);
		}
	}
	applyUrl('', index);
	applyUrl('/games', index);
	applyUrl('/game', gameForm);
	applyUrl('/game/:id', gameDetail);
	applyUrl('/event', gameEvent);
	dashboard.addRoutes(applyUrl);
	applyUrl('/event/new', newEvent);
};

