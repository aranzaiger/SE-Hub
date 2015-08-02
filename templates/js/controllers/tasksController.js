angular.module('SeHub')
.controller('tasksController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.lecturerTasks = [];
	$rootScope.seToken = $cookies['com.sehub.www'];
  	var token = $rootScope.seToken;

	$scope.createTaskClicked = function()
	{
		$location.path("/tasks/new"); // Reference to 'newTask' page
	}

	$scope.displayTasks = function()
	{
	    apiService.getAllFutureTasks(token).success(function(data) // Get all Tasks // TODO change to closest TASK
	    {
	      $scope.lecturerTasks = data;
	      console.log(data);
	    }).error(function(err)
	    {
	      console.log(err.message);
	    });
	}
	$scope.gotoTask = function(taskId)
	{
		$location.path('/tasks/fill/' + taskId);
	}

	$scope.displayTasks(); // Calling tasks with task id


}]);