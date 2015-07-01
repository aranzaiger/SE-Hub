angular.module('SeHub')
.controller('tasksController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	console.log("in controller");

	$scope.createTaskClicked = function()
	{
		$location.path("/tasks/new"); // Reference to 'newTask' page
	}




}]);