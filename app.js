
/**
 * Module dependencies.
 */

var express = require('express'),
	urls = require('./routes/urls'),
	http = require('http'),
	path = require('path'),
	titterConnect = require('./lib/twitter-connect');



var app = express();

app.configure(function(){
	app.use(express.compress());
	app.set('port', process.env.PORT || 3000);
	app.set('views', __dirname + '/views');
	app.set('view engine', 'ejs');
	app.use(express.favicon());
	app.use(express.logger('dev'));
	app.use(express.bodyParser());
	app.use(express.methodOverride());
	app.use(express.cookieParser());
	app.use(express.session({ secret: 'keyboard cat' }));

	// add the twitter support
	titterConnect.patchApp(app);

	app.use(app.router);

	app.use(require('stylus').middleware(__dirname + '/public'));
	app.use(express.static(path.join(__dirname, 'public')));
});

app.configure('development', function(){
	app.use(express.errorHandler());
});


urls.applyUrls(app);
titterConnect.setRoutes(app);


var models = require("./lib/models");

http.createServer(app).listen(app.get('port'), function() {
	models.connect();
	console.log("Express server listening on port " + app.get('port'));
});
