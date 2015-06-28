angular.module('SeHub')
.controller('thisProjectController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.isEditPressed = false;
	$scope.myProjectsEmpty = false;
	var token = $cookies['com.sehub.www'];




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
			myProjectsEmpty = true;
		}
	}

	$scope.goToMyProject = function()
	{
		console.log("projects only from classID: "  + classId)
		$location.path('/thisProject' + classId);
	}

	var init = function()
	{
		var i, j, counter = 0;
		var newLength = 0;
		
		if(($scope.projects.length % 3) === 0)
		{
			newLength = ($scope.projects.length / 3);
		}
		else
		{
			newLength = (Math.ceil($scope.projects.length / 3)); // Rounds number up
		}
		
		console.log("length: " + newLength);
		$scope.arrayHolder.length = newLength;

		for(j = 0; j < newLength; j++)	
		{
			$scope.arrayHolder[j] = [3]; // Creating array in size of 3 in each array cell
		}

		for(i = 0; i < newLength; i++)		
		{		
			for(j = 0; j < newLength; j++)
			{
				if($scope.projects[(3*i) + j] != null)
				{	
					$scope.arrayHolder[i][j] = $scope.projects[(3*i) + j];
				}
			}	
		}
		console.log($scope.arrayHolder);
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