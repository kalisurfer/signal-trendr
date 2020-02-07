var passport = require('passport'),
	TwitterStrategy = require('passport-twitter').Strategy,
	eventManager = require('./events').eventManager,
	Twitter = require("twitter-js-client").Twitter;


var TWITTER_CONSUMER_KEY = "MIzpe0HomjqE3AZ7sqzdTQ";
var TWITTER_CONSUMER_SECRET = "4AHlHwZVPeQ3GZG1RERd98KZQaV6pSRYc0980smH0";

var models = require("../lib/models"),
	User = models.models.User;


var host_info = (process.env.SERVICE_HOST || "localhost") + ":" + (process.env.PORT || 3000);

passport.use(new TwitterStrategy({
    consumerKey: TWITTER_CONSUMER_KEY,
    consumerSecret: TWITTER_CONSUMER_SECRET,
    callbackURL: "http://" + host_info + "/auth/twitter/callback"
  },
  function(token, tokenSecret, user, done) {
	User.findOne({twitterId: Number(user.id)}).exec(function(err, profile) {
		var is_new = false;
		if(err || !profile) {
			profile = new User({twitterId: Number(user.id), username: user.username});
			try {
				profile.photo = user.photos[0].value;
			} catch(e) {
				console.log("user has no photos", user.photos);
			}
			is_new = true;
		}
		profile.raw = user;
		profile.token = token;
		profile.tokenSecret = tokenSecret;
		
		var twitter = new Twitter({
			"consumerKey": TWITTER_CONSUMER_KEY,
			"consumerSecret": TWITTER_CONSUMER_SECRET,
			"accessToken": token,
			"accessTokenSecret": tokenSecret,
		});
		function finish(err, list) {
			if(list) {
				list = JSON.parse(list);
				console.log("setting friends", list);
				profile.friends = list.ids;
			}
			profile.save(function(err, prof) {
				done(err, prof);
				if(is_new) {
					eventManager.trigger('new_user', {user: prof});
				}
			});
		}
		twitter.doRequest(twitter.baseUrl + "/friends/ids.json", function(err) { finish(err, null); }, function(body) { finish(null, body); });
	});
  }
));

// Passport session setup.
//   To support persistent login sessions, Passport needs to be able to
//   serialize users into and deserialize users out of the session.  Typically,
//   this will be as simple as storing the user ID when serializing, and finding
//   the user by ID when deserializing.  However, since this example does not
//   have a database of user records, the complete Twitter profile is serialized
//   and deserialized.
passport.serializeUser(function(user, done) {
	done(null, user.id);
});

passport.deserializeUser(function(obj, done) {
	User.findOne({_id: obj}).exec(function(err, profile) {
		if(profile) {
			done(err, profile);
		} else {
			done("not found", null);
		}
	});
});




exports.patchApp = function(app) {
		app.use(passport.initialize());
		app.use(passport.session());
	};

exports.setRoutes = function(app) {
		app.get('/auth/twitter', passport.authenticate('twitter'));
		app.get('/auth/twitter/callback', passport.authenticate('twitter', { successReturnToOrRedirect: '/', failureRedirect: '/login' }));


		// GET /auth/twitter
		//   Use passport.authenticate() as route middleware to authenticate the
		//   request.  The first step in Twitter authentication will involve redirecting
		//   the user to twitter.com.  After authorization, the Twitter will redirect
		//   the user back to this application at /auth/twitter/callback
		app.get('/auth/twitter',
			passport.authenticate('twitter'),
			function(req, res){
				//The request will be redirected to Twitter for authentication, so this
				//function will not be called.
			});

		// GET /auth/twitter/callback
		//   Use passport.authenticate() as route middleware to authenticate the
		//   request.  If authentication fails, the user will be redirected back to the
		//   login page.  Otherwise, the primary route function function will be called,
		//   which, in this example, will redirect the user to the home page.
		app.get('/auth/twitter/callback',
			passport.authenticate('twitter', { failureRedirect: '/login' }),
			function(req, res) {
				res.redirect('/');
		});

		app.get('/logout', function(req, res){
			req.logout();
			res.redirect('/');
		});
	};