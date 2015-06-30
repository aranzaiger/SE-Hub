angular.module('SeHub')
.controller('projectController', ['$scope', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
 function ($scope, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	var token = $cookies['com.sehub.www'];
	var projectId = $routeParams.projectId;
	$scope.isEditPressed = false;
	$scope.user = $scope.$parent.user;
	$scope.loadingData = true;
	$scope.isMasterOrLecturer = false;

	// $scope.thisProject = {};
	// $scope.thisProject.courseName = $routeParams.className;

	$scope.editProject = function(ev)
	{
		$scope.isEditPressed = true;
		console.log("EditPressed " + $scope.isEditPressed);
	}

	$scope.removeProject = function(ev)
	{
		console.log("Project has been removed!");
		$mdDialog.show($mdDialog.alert().title('Remove Project').content('Are you sure you want to remove the project ?')
		.ariaLabel('Removing project alert dialog').ok('Yes').targetEvent(ev));
		// .then(function() {
			// $location.path('/class/' + data.id + '/' + data.courseName); // Will display all the projects in this course
		// }); // Pop-up alert
	};

	

	$scope.getProjectInfo = function()
	{
		apiService.getProjectsById(token, projectId).success(function(data)
		{
			$scope.project = data;
			console.log($scope.project);
			$scope.init_line_lables();
			// if($scope.user === $scope.project.info.master_id)
			// {
			// 	$scope.isMasterOrLecturer = true;
			// }
			// if($scope.project && $scope.project.length > 0) // TODO - TEST?
			// {
				$scope.loadingData = false;
			// }
			
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