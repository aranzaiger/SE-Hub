angular.module('SeHub')
.controller('projectsContoller', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	console.log("in projects controller");

	$scope.createProjectClicked = function()
	{
		console.log("project created! not rly!! ");
		// $window.location.href = 'http://localhost:8080/home#/tasks/new'; // Reference to 'newTask' page

	}




}]);