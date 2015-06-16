var DEBUG = true;

var welcome = angular.module('welcome', ['ngMaterial', 'seHub.services', 'ngRoute' , 'ngCookies']);

var app = angular.module('SeHub', ['ngMaterial', 'ngRoute', 'seHub.services', 'ngCookies']);


welcome.config(function($mdThemingProvider) {
	$mdThemingProvider.theme('default')
		.primaryPalette('teal');
});

welcome.controller('welcomeController', ['$scope', 'apiService', '$cookies', '$window', function($scope, apiService, $cookies, $window) {
	console.log("Welcome Controller");

	var uid = $cookies['com.sehub.www'];
	if(uid){
		console.info("Session in Place");
		$window.location.href = DEBUG ? 'http://localhost:8080/home' : 'http://se-hub.appspot.com/home';
	}



}]);


app.config(['$routeProvider', '$locationProvider',
	function($routeProvider, $locationProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'templates/views/home.html'
			})
			.when('/register', {
				templateUrl: 'templates/views/register.html',
				controller: 'registerController'
			})
			.when('/home', {
				templateUrl: 'templates/views/home.html',
				controller: 'homeController'
			});

	}
]);

