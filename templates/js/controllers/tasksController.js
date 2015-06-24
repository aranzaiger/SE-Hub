angular.module('SeHub')
.controller('tasksController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	console.log("in controller");

	$scope.createTaskClicked = function(name)
	{
		var taskName = name;
		console.log("task created! " + taskName);
		$location.path("/tasks/new"); // Reference to 'newTask' page

	}




}]);