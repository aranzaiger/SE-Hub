angular.module('SeHub')
.controller('registerController', ['$scope', 'apiService', '$rootScope', function ($scope, apiService ,$rootScope) {
	
	$scope.userHasNoName = false;
	$scope.campusChecked = false;
	$scope.isEmpty = true; // if the academic email line is empty
	// $scope.fullMail = $scope.academicEmail + $scope.campusObj.email_ending; // Will hold the full academic email of the user


	$scope.user = $rootScope.user;
	if($scope.user.name === ";"){
		$scope.user.name = "";
		$scope.user.name = $scope.user.username
		$scope.userHasNoName = true;
	};

	$scope.dropdownClicked = function()
	{
			// console.log($scope.fullMail);
		if($scope.campus){
			$scope.campusChecked = true;
			$scope.campusObj = null;
			for (var i = $scope.campuses.length - 1; i >= 0; i--) {
				if($scope.campuses[i].title == $scope.campus){
					$scope.campusObj = $scope.campuses[i];
					console.log($scope.campusObj);
				}
			};
		}
		
	};

	$scope.submitClicked = function()
	{
		console.log($scope.user.AcMail);

	};

	apiService.getAllCampuses($scope.user.seToken).success(function(data)
	{
		$scope.campuses = data;
	}).error(function()
	{
		// TODO
	});

	// apiService.sendValidationMail($scope.user.seToken, $scope.fullMail).success(function(data) // TODO: Add 2nd parameter email type Email
	// {
	// 	console.log($scope.fullMail);
	// 	console.log("200");
		
	// 	// TODO
	// }).error(function()
	// {

	// });


	


}]);																						