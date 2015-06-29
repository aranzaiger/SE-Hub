angular.module('SeHub')
.controller('myProjectsController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.isEditPressed = false;
	$scope.loadingData = true;
	$scope.myProjectsEmpty = true;
	$scope.user = $scope.$parent.user;
	var token = $cookies['com.sehub.www'];
	console.log(token);

	$scope.displayMyProjects = function()
	{
		apiService.getProjectsByUser(token).success(function(data)
		{
			$scope.loadingData = false;
			$scope.myProjects = data;
			if($scope.myProjects != null && $scope.myProjects.length > 0)
			{
				$scope.myProjectsEmpty = false;
			}
			init();  // Executing the function to initialize my projects display
			console.log(data);
			console.log("Success");
		}).error(function(err)
		{
			console.log("Error: " + err.message);
		});
		
	}

	$scope.goToProject = function(projectId)
	{
		for (var i = 0; i < $scope.myProjects; i++)
		{
			if($scope.myProjects.id === projectId)
			{
				console.log("project ID: "  + projectId)
				$location.path('/project/' + projectId);
			}
		};
	}

	var init = function()
	{
		$scope.arrayHolder = [];
		var tempArr = [];
		var sizeOfSmallArrays = 3;
		for (var i = 0 ; i < $scope.myProjects.length ; i++) {
			if(i % sizeOfSmallArrays !== 0){
				tempArr.push($scope.myProjects[i]);
			}else{
				if(i !== 0){
					$scope.arrayHolder.push(tempArr);
					tempArr = [];
					tempArr.push($scope.myProjects[i]);
				}else{
					tempArr.push($scope.myProjects[i]);
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