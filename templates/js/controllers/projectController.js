angular.module('SeHub')
.controller('projectController', ['$scope', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
 function ($scope, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	var token = $cookies['com.sehub.www'];
	var projectId = $routeParams.projectId;
	$scope.isEditPressed = false;
	$scope.user = $scope.$parent.user;
	$scope.loadingData = true;

	// $scope.thisProject = {};
	// $scope.thisProject.courseName = $routeParams.className;

	$scope.editProject = function()
	{
		$scope.isEditPressed = true;
		console.log("EditPressed " + $scope.isEditPressed);
	}
	$scope.removeProject = function()
	{
		console.log("Project has been removed!");
	}

	$scope.getProjectInfo = function()
	{
		apiService.getProjectsById(token, projectId).success(function(data)
		{
			$scope.project = data;
			console.log($scope.project);
			$scope.init_line_lables();
			$scope.loadingData = false;
			console.log($scope.project);
		}).error(function(err)
		{
			console.log("Error: " + err.message);
		});
	}

	$scope.init_line_lables = function(){
		$scope.project.weekly_labels = [];
		for(var i = 0 ; i < $scope.project.info.stats.weekly_commits[0].length; i++)
			$scope.project.weekly_labels.push('w '+i.toString());

	}

	$scope.getProjectInfo(); // Get all this project data
}]);