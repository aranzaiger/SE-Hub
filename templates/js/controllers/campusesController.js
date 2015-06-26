angular.module('SeHub')
.controller('campusesController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope)
{
	$scope.threeSizedArray =[];
	var token = $cookies['com.sehub.www'];
	
	$scope.campuses = ['Bezalel', 'Ben Gurion', 'Sami Shamoon', 'Afeka', 'Ivrit', 'Kaka', 'Opium']; // TODO REMOVE
	

	// apiService.getCampusesByUser().success(function(data) // Get all the campuses
	// {
	// 	console.log("INSIDE");
	// 	$scope.campuses = data;
	// }).error(function() {
	// // TODO
	// });
	console.log($scope.campuses);


	var init = function()
	{
		var i, j, counter = 0;
		var newLength = 0;
		
		if(($scope.campuses.length % 3) === 0)
		{
			newLength = ($scope.campuses.length / 3);
		}
		else
		{
			newLength = (Math.ceil($scope.campuses.length / 3)); // Rounds number up
		}
		
		console.log("length: " + newLength);
		$scope.threeSizedArray.length = newLength;

		for(j = 0; j < newLength; j++)	
		{
			$scope.threeSizedArray[j] = [3]; // Creating array in size of 3 in each array cell
		}

		for(i = 0; i < newLength; i++)		
		{		
			for(j = 0; j < newLength; j++)
			{
				if($scope.campuses[(3*i) + j] != null)
				{	
					$scope.threeSizedArray[i][j] = $scope.campuses[(3*i) + j];
				}
			}	
		}
		console.log($scope.threeSizedArray);
	}

	init(); // Executing the function to initialize campuses show



}]);
