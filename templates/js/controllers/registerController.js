angular.module('SeHub')
.controller('registerController', ['$scope', '$location', '$cookies', 'apiService', '$rootScope', function ($scope, $location, $cookies, apiService ,$rootScope) {
	
	$scope.userHasNoName = false;
	$scope.campusChecked = false;
	$scope.isEmpty = true; // if the academic email line is empty
	

	$rootScope.seToken = $cookies['com.sehub.www'];
	var token = $rootScope.seToken;

	apiService.getUserByToken(token).success(function(data){
		$scope.user = data;
				console.log(data);
		if(data.message == 'No User Found')
			console.error("No User Found!");

		$scope.user = data;
		$rootScope.user = data;
		if($scope.user.isFirstLogin)
			$location.path('/register')


		if($scope.user.name === ";"){
			$scope.user.name = "";
			$scope.user.name = $scope.user.username
			$scope.userHasNoName = true;
		}

	apiService.getAllCampuses($scope.user.seToken).success(function(data)
	{
		$scope.campuses = data;
	}).error(function()
	{
		// TODO
	});

	});


	

	$scope.dropdownClicked = function()
	{
		if($scope.campus){
			$scope.campusChecked = true;
			$scope.campusObj = null;
			for (var i = $scope.campuses.length - 1; i >= 0; i--) {
				if($scope.campuses[i].title == $scope.campus){
					$scope.campusObj = $scope.campuses[i];
					console.log($scope.campusObj); // TODO REMOVE!!
				}
			};
		}
		
	};

	$scope.submitClicked = function()
	{
		$scope.mail = 'pin';
		console.log($scope.mail);
	};

	// apiService.sendValidationMail($scope.user.seToken, $scope.fullMail).success(function(data) // TODO: Add 2nd parameter email type Email
	// {
	// 	console.log($scope.fullMail);
	// 	console.log("200");
		
	// 	// TODO
	// }).error(function()
	// {

	// });


	


}]);