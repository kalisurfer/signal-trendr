

var Events = require('backbone').Events,
	_ = require("underscore");

var eventManager = {};

_.extend(eventManager, Events);

eventManager.on("new_user", function(user) {
	/*
	 *  The idea here is that we can add this user to a queue that will process later
	 *  and check to see if this new user is followed by of any existing users. We will
	 *  then notify the existing user.
	 *
	 *  From here we can also send out the welcome email, or queue it up anyway.
	 */
	console.log("we got a new user, what do we do with them?", user.twitterId);
});


exports.eventManager = eventManager;
