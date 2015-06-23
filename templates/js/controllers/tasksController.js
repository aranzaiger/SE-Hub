angular.module('SeHub')
.controller('tasksController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	console.log("in controller");

	$scope.createTaskClicked = function(name)
	{
		var taskName = name;
		console.log("task created! " + taskName);
		$window.location.href = 'http://localhost:8080/home#/tasks/new'; // Reference to 'newTask' page

	}




}]);