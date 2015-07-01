angular.module('SeHub')
.controller('campusesController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope)
{
	$scope.loadingData = true;
	$scope.campusesEmpty = false;
	var token = $cookies['com.sehub.www'];
	
	var init = function()
	{
		$scope.threeSizedArray = [];
		var tempArr = [];
		var sizeOfSmallArrays = 3;
		for (var i = 0 ; i < $scope.campuses.length ; i++) {
			if(i % sizeOfSmallArrays !== 0){
				tempArr.push($scope.campuses[i]);
			}else{
				if(i !== 0){
					$scope.threeSizedArray.push(tempArr);
					tempArr = [];
					tempArr.push($scope.campuses[i]);
				}else{
					tempArr.push($scope.campuses[i]);
				}
			}
		};
		$scope.threeSizedArray.push(tempArr);
	}

	$scope.goToCampus = function(campusId) // Will pass you to courses by specific campus
	{
		$location.path('/myClasses/' + campusId.toString());
	}

	$scope.displayCampuses = function()
	{
		apiService.getCampusesByUser(token).success(function(data) // Get all the campuses
		{
			$scope.loadingData = true;
			$scope.campuses = data;
			console.log("INSIDE " + $scope.campuses);
			init(); // Executing the function to initialize campuses display
			
		}).error(function()
		{
			// TODO
		});
		// console.log($scope.campuses.length.toString());

		if(!$scope.campuses) // If campuses is empty
		{
			$scope.campusesEmpty = true;
		}
	}

	$scope.displayCampuses(); // Displaying all campuses by user



}]);
