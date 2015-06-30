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
	}

	$scope.removeProject = function(ev)
	{
		$mdDialog.show($mdDialog.alert().title('Remove Project').content('Are you sure you want to remove the project ?')
		.ariaLabel('Removing project alert dialog').ok('Yes').targetEvent(ev));
		// .then(function() {
			// $location.path('/class/' + data.id + '/' + data.courseName); // Will display all the projects in this course
		// }); // Pop-up alert
	};

	$scope.getProfileRoute = function(assigneeName)
	{
		for(var i = 0; i < $scope.project.members.length; i++)
		{
			
			if(assigneeName === $scope.project.members[i].name)
			{
				console.log(assigneeName);
				console.log($scope.project.members[i].name);
				return '#/profile/' + $scope.project.members[i].id;
			}
			else
				return '#';
		}
	}

	$scope.getProjectInfo = function()
	{
		apiService.getProjectsById(token, projectId).success(function(data)
		{
			$scope.project = data;
			// if($scope.user === $scope.project.info.master_id)
			// {
			// 	$scope.isMasterOrLecturer = true;
			// }
			// if($scope.project && $scope.project.length > 0) // TODO - TEST?
			// {
				$scope.loadingData = false;
			// }
		}).error(function(err)
		{
			console.log("Error: " + err.message);
		});
	}

	$scope.getProjectInfo(); // Get all this project data
}]);