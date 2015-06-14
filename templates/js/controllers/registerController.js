angular.module('SeHub')
.controller('registerController', ['$scope', '$cookies', 'apiService', '$rootScope', function ($scope, $cookies, apiService ,$rootScope) {
	
	$scope.userHasNoName = false;
	$scope.campusChecked = false;
	$scope.isEmpty = true; // if the academic email line is empty

	$rootScope.seToken = $cookies['com.sehub.www'];
	var token = $rootScope.seToken;

	apiService.getUserByToken(token).success(function(data){
		$scope.user = data;
		
		if(data.message == 'No User Found')
			console.error("No User Found!");
		console.log(data);

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
		};
	};

	$scope.submitClicked = function()
	{
		if($scope.user.AcMail != null)
		{
			var fullMail = $scope.user.AcMail + $scope.campusObj.email_ending; // Holds the full academic email of the user
			apiService.sendValidationMail($scope.user.seToken, fullMail).success(function(data) // TODO: Add 2nd parameter email type Email
			{
				console.log("DONE - 200");	
				// TODO - add a window that display that an email has been sent for verification
			}).error(function()
			{
				// TODO
			});
		};
	};




	


}]);																						