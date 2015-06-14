angular.module('SeHub')
.controller('registerController', ['$scope', '$cookies', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	
	$scope.userHasNoName = false;
	$scope.campusChecked = false;
	$scope.isEmpty = true; // if the academic email line is empty

	$rootScope.seToken = $cookies['com.sehub.www'];
	var token = $rootScope.seToken;

	apiService.getUserByToken(token).success(function(data) // Get user token
	{
		$scope.user = data;
		
		if(data.message == 'No User Found')
			console.error("No User Found!");
		console.log(data);

		if($scope.user.name === ";")
		{
			$scope.user.name = "";
			$scope.user.name = $scope.user.username
			$scope.userHasNoName = true;
		}

		apiService.getAllCampuses($scope.user.seToken).success(function(data) // Get all the campuses
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

	$scope.submitClicked = function(ev)
	{
		if($scope.user.AcMail != null)
		{
			var fullMail = $scope.user.AcMail + $scope.campusObj.email_ending; // Holds the full academic email of the user
			apiService.sendValidationMail($scope.user.seToken, fullMail).success(function(data)
			{
				console.log("DONE - 200");
			  	$mdDialog.show($mdDialog.alert().title('E-mail Verification').content('A verification e-mail has been sent to your email address.')
		        .ariaLabel('Email verification alert dialog').ok('Got it!').targetEvent(ev));
		        // TODO - ADD DELETE COOKIES
		        // $cookies.remove("com.sehub.www");
		        // $location.path("templates/views/home.html"); // Redirecting to home page // TODO REMOVE REMOVE!!
			}).error(function()
			{
				$mdDialog.show($mdDialog.alert().title('Error - E-mail Verification').content('An error has occured in your e-mail address.')
		        .ariaLabel('Email verification error alert dialog').ok('Got it!').targetEvent(ev));
			});
		};
	};


	// TODO FOR LATER
	// TODO FOR LATER

	$scope.getPopWindowPosition = function()
  	{
    	return Object.keys($scope.toastPosition).filter(function(pos)
    		{
    			return $scope.toastPosition[pos];
    		}).join(' ');
  	};
  	
  	$scope.toastPosition =
  	{
	    bottom: false,
	    top: true,
	    left: false,
	    right: true
  	};

  	// TODO FOR LATER
  	// TODO FOR LATER

	
}]);


