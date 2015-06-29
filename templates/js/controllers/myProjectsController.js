angular.module('SeHub')
.controller('myProjectsController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.isEditPressed = false;
	$scope.myProjectsEmpty = false;
	var token = $cookies['com.sehub.www'];

	$scope.user = $scope.$parent.user;

	$scope.displayMyProjects = function()
	{
		apiService.getProjectsByUser(token).success(function(data)
		{
			console.log("Success " + data);
			$scope.myProjects = data;
		}).error(function(err)
		{
			console.log("Error: " + err);
		});
		if($scope.myProjects === null)
		{
			$scope.myProjectsEmpty = true;
		}
	}

	$scope.goToMyProject = function()
	{
		console.log("projects only from classID: "  + classId)
		$location.path('/thisProject' + classId);
	}

	var init = function()
	{
		$scope.arrayHolder = [];
		var tempArr = [];
		var sizeOfSmallArrays = 3;
		for (var i = 0 ; i < $scope.projects.length ; i++) {
			if(i % sizeOfSmallArrays !== 0){
				tempArr.push($scope.projects[i]);
			}else{
				if(i !== 0){
					$scope.arrayHolder.push(tempArr);
					tempArr = [];
					tempArr.push($scope.projects[i]);
				}else{
					tempArr.push($scope.projects[i]);
				}
			}
		};
		$scope.arrayHolder.push(tempArr);
	}

	$scope.editPressed = function()
	{
		$scope.isEditPressed = true;
		console.log("EditPressed " + $scope.isEditPressed);
	}
	$scope.removeProject = function()
	{
		console.log("Project has been removed!");
	}


	$scope.displayMyProjects(); // Will display all my projects

}]);