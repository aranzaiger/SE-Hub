angular.module('SeHub')
.controller('campusesController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope)
{
	$scope.threeSizedArray =[];
	$scope.campusesEmpty = false;
	var token = $cookies['com.sehub.www'];

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
		console.log($scope.threeSizedArray); // TODO REMOVE
	}

	$scope.goToCampus = function(campusId) // Will pass you to courses by specific campus
	{
		$location.path('/myClasses/' + campusId.toString());
	}

	$scope.displayCampuses = function()
	{
		apiService.getCampusesByUser(token).success(function(data) // Get all the campuses
		{
			$scope.campuses = data;
			console.log("INSIDE " + $scope.campuses);
			init(); // Executing the function to initialize campuses display
			
		}).error(function()
		{
			// TODO
		});
		if($scope.campuses != null)
		{
			$scope.campusesEmpty = true;
		}
	}

	$scope.displayCampuses(); // Displaying all campuses by user



}]);
