var weareAdminControllers = angular.module('weareAdminControllers', []);


// function getParameterByName(name) {
//     name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
//     var regexS = "[\\?&]" + name + "=([^&#]*)";
//     var regex = new RegExp(regexS);
//     var results = regex.exec(window.location.search);
//     if (results === null) {
//         return "";
//     }
//     return decodeURIComponent(results[1].replace(/\+/g, " "));
// }


weareAdminControllers.controller('trendingCtrl', function ($scope, $location, $http) {
	$http.get('/admin/dashboard/data/games/trending').success(function(response) {
		$scope.trending = response.games;
	});
});

weareAdminControllers.controller('mainRankingsCtrl', function ($scope, $location, $http) {
	$http.get('/admin/dashboard/data/list/main').success(function(response) {
		$scope.mainRankings = response.games;
	});
});

weareAdminControllers.controller('mentionsCtrl', function ($scope, $location, $http) {
	$http.get('/admin/dashboard/data/games/mentions/top').success(function(response) {
		$scope.mentions = response.games;
	});
});

weareAdminControllers.controller('yesterdayTrendingCtrl', function ($scope, $location, $http) {
	$http.get('/admin/dashboard/data/games/movers').success(function(response) {
		$scope.games = response.games;
	});
});

weareAdminControllers.controller('recentEventsCtrl', function ($scope, $location, $http) {
	$http.get('/admin/dashboard/data/events').success(function(response) {
		$scope.events = response.events;
	});
});

weareAdminControllers.controller('recentVideosCtrl', function ($scope, $location, $http) {
	$http.get('/admin/dashboard/data/videos').success(function(response) {
		$scope.videos = response.videos;
	});
});

weareAdminControllers.controller('recentEditorialsCtrl', function ($scope, $location, $http) {
	$http.get('/admin/dashboard/data/editorials').success(function(response) {
		$scope.tweets = response.tweets;
	});
});

