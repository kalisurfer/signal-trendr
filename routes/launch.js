/*
 * GET About Page
 */

 /* this page gives a brief backstory on what we are trying to do and who we are */
 
var inspect = require('sys').inspect;

exports.index = function(req, res) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		context = {title: 'We Are Playing It', submitted: "False", data: [], user: req.user};
		context["rankingTitle"] = 'Meet WeArePlayingIt, a service dedicated to helping you discover that next video game you will lose, sleep, significant others and your job over.';

	res.render('launch', context);
};

exports.thankyou = function(req, res) {
	var models = require("../lib/models"),
		Game = models.models.Game,
		context = {title: 'We Are Playing It', submitted: "True", data: [], user: req.user};
		context["rankingTitle"] = 'Thank you for signing up.  Please spread the word and keep checking back.';

	res.render('launch', context);
};
