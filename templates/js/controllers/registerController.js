angular.module('SeHub')
.controller('registerController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.userHasNoName = false;
	$scope.campusChecked = false;
	$scope.createCampusClicked = false;
	$scope.isEmpty = true; // if the academic email line is empty
	$scope.jsonCreateCampus =
			{
				"title": "Create Campus",
				"email": "email_ending",
				"avatar": "self.avatar.url"
			}

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
		        .ariaLabel('Email verification alert dialog').ok('Got it!').targetEvent(ev)); // Pop-up alert for e-mail verification
		        // TODO ADD delete cookies and redirect only after pressed 'Got it'
		        $cookieStore.remove("com.sehub.www"); // Removing the cookies
		        $window.location.href = 'http://se-hub.appspot.com'; // Reference to 'welcome' page
			}).error(function()
			{
				$mdDialog.show($mdDialog.alert().title('Error - E-mail Verification').content('An error has occured in your e-mail address.')
		        .ariaLabel('Email verification error alert dialog').ok('Got it!').targetEvent(ev));
			});
		};
	};


	$scope.lecturer = function(ev)
	{
		console.log("inside");
		$scope.createCampusClicked = true;

		if(!$scope.isLecturer) // if i am a lecturer (when pressing -> getting last data value before pressing) = "!isLecturer" it means => I Am Lecturer
		{
			// var jsonCreateCampus =
			// {
			// 	"title": "Create Campus",
			// 	"email": "email_ending",
			// 	"avatar": "self.avatar.url"
			// }
			console.log("YES lecturer " + $scope.jsonCreateCampus.title);

			if($scope.user.lecAcMail != null)
			{
				apiService.sendValidationMail($scope.user.seToken, $scope.user.lecAcMail).success(function(data)
				{
					console.log("DONE - 200");
				  	$mdDialog.show($mdDialog.alert().title('E-mail Verification').content('A verification e-mail has been sent to your email address.')
			        .ariaLabel('Email verification alert dialog').ok('Got it!').targetEvent(ev)); // Pop-up alert for e-mail verification
			        // TODO ADD delete cookies and redirect only after pressed 'Got it'
			        $cookieStore.remove("com.sehub.www"); // Removing the cookies
			        $window.location.href = 'http://se-hub.appspot.com'; // Reference to 'welcome' page
				}).error(function()
				{
					$mdDialog.show($mdDialog.alert().title('Error - E-mail Verification').content('An error has occured in your e-mail address or in the campus name.')
			        .ariaLabel('Email verification error alert dialog').ok('Got it!').targetEvent(ev));
				});
			}
		}
	}  	
}]);
