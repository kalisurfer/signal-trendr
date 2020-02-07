var weareNow = angular.module('weareNow', ['linkify']);

weareNow.filter('moment', function() {
    return function(dateString, format) {
        return moment(dateString).fromNow(format);
    };
});


weareNow.controller('nowCtrl', function ($scope, $location, $http) {
	var nextToLoad = 1;
	$scope.tweets = [];
	$scope.getMore = function() {
		console.log("loading more tweets");
		$http.get('/now/' + nextToLoad).success(function(response) {
			if(response.hasOwnProperty("tweets")) {
				console.log(response);
				_.each(response.tweets, function(tweet) {
					tweet.media_url = "";
					var media = tweet.media;
					if (typeof media == "object") {
						var media_url = "";
						for (var i=0;i<media.length;i++) {
							if (media[i].media_url !== "") {
								media_url = media[i].media_url;
								break;
							}
						}
						if (media_url !== "") {
							tweet.media_url = media_url;
						}
					}
				});
				$scope.tweets = $scope.tweets.concat(response.tweets);
				console.log("$scope.tweets", $scope.tweets.length);
				imagesLoaded($('#masonryContainer'), function() {
					// $('#masonryContainer').masonry( 'appended', $('#masonryContainer div.columns') );
					$('#masonryContainer').masonry("reloadItems");
					$('#masonryContainer').masonry("layout");
				});
			}
		});
		nextToLoad += 1;
		console.log(nextToLoad);
	};
	
	// $('#masonryContainer').masonry({
	//         columnWidth: '.large-3',
 //      		itemSelector: '.columns'
 //    	});

	$scope.getMore();

	//setInterval(function() { $('#masonryContainer').masonry("layout"); }, 1000);

	$scope.rankTweet = function(tweet) {
		var score = tweet.score;
        var style = "";
        if (score >= 150) {
          style = "background-color: red; width:200px;";
        } else if (score >= 100) {
          style = "background-color: orange; width:150px;";
        } else if (score >= 50) {
          style = "background-color: yellow; width:100px;";
        } else {
          style = "background-color: teal; width:50px;";
        }
        return style;
    };


});
