angular.module('SeHub')
.controller('campusesController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope) {




	$scope.campuses = ['Bezalel', 'Ben Gurion', 'Sami Shamoon', 'Afeka', 'Ivrit', 'Kaka', 'Opium'];
	console.log($scope.campuses);

	// apiService.getCampusesByUser(token).success(function(data) // Get all the campuses
	// {
	// 	$scope.campuses = data;
	// }).error(function() {
	// // TODO
	// });

}]);