
/*
 * GET About Page
 */

 /* this page gives a brief backstory on what we are trying to do and who we are */
 
var inspect = require('sys').inspect;
var filter = "trendIndex";

exports.index = function(req, res) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		context = {title: 'About We Are Playing It', data: [], user: req.user};
		context["rankingTitle"] = 'Our Philosophy and Team';

	res.render('about', context);
};

exports.list = require("./about").index;