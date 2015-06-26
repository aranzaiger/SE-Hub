angular.module('SeHub')
.controller('projectsController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	console.log("in projects controller");

	$scope.createProjectClicked = function()
	{
		console.log("project created! not rly!! ");
		// $window.location.href = 'http://localhost:8080/home#/tasks/new'; // Reference to 'newTask' page

	}

	$scope.projects = ['AMI', 'LULU', 'XIN Zhau', 'LUMI lu', 'Shimi', 'Azligi zligi', 'Drugs'];

	// apiService.getProjectsByCourse(courseId).success(function(data) // Get all the campuses
	// {
	// 	$scope.projects = data;
	// }).error(function() {
	// // TODO
	// });

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

	init(); // Executing the function to initialize projects display


}]);