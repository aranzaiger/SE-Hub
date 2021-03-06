angular.module('SeHub')
	.controller('registerController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
		function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope) {
		$scope.userHasNoName = false;
		$scope.campusChecked = false;
		$scope.createCampusClicked = false;
		$scope.isEmpty = true; // if the academic email line is empty
		$scope.jsonCreateCampus = {
			"title": "Create Campus",
			"email": "email_ending",
			"avatar": "self.avatar.url"
		}

		$rootScope.seToken = $cookies['com.sehub.www'];
		var token = $rootScope.seToken;

		apiService.getUserByToken(token).success(function(data) // Get user token
		{
			$scope.user = data;

			if (data.message == 'No User Found')
				console.error("No User Found!");
			console.log(data);

			if ($scope.user.name === ";") {
				$scope.user.name = "";
				$scope.user.name = $scope.user.username;
				$scope.userHasNoName = true;
			}

			apiService.getAllCampuses(token).success(function(data) // Get all the campuses
			{
				$scope.campuses = data;
			}).error(function() {
				// TODO
			});
		});

		$scope.dropdownClicked = function() {
			$scope.createCampusClicked = false;
			if($scope.campus) {
				$scope.campusChecked = true;
				$scope.campusObj = null;
				for (var i = $scope.campuses.length - 1; i >= 0; i--) {
					if ($scope.campuses[i].title == $scope.campus) {
						$scope.campusObj = $scope.campuses[i];
						console.log($scope.campusObj); // TODO REMOVE!!
					}
				};
			};
		};

		$scope.submitClicked = function(ev) {
			var emailValid = false;

			if ($scope.user.AcMail != null) {
				var fullMail = $scope.user.AcMail + $scope.campusObj.email_ending; // Holds the full academic email of the user
				apiService.updateUser(token, $scope.user).success(function(data) {
				}).error(function() {
				});

				console.log("Mail: " + fullMail);

				apiService.sendValidationMail(token, fullMail).success(function(data) {
					console.log("DONE - 200");
					$mdDialog
						.show($mdDialog.alert().title('E-mail Verification')
							.content('A verification e-mail has been sent to your email address.')
							.ariaLabel('Email verification alert dialog')
							.ok('Got it!')
							.targetEvent(ev))
						.then(function() {
							$cookieStore.remove("com.sehub.www"); // Removing the cookies
							$window.location.href = 'http://se-hub.appspot.com'; // Reference to 'welcome' page

						}); // Pop-up alert for e-mail verification
				}).error(function() {
					$mdDialog.show($mdDialog.alert().title('Error - E-mail Verification').content('An error has occured in your e-mail address.')
						.ariaLabel('Email verification error alert dialog').ok('Got it!').targetEvent(ev));
				});
			} else // TODO Fix when success to show mdDialog until 'Got it' clicked
			{
				$mdDialog.show($mdDialog.alert().title('Error - E-mail Verification').content('An error has occured in your e-mail address.')
					.ariaLabel('Email verification error alert dialog').ok('Got it!').targetEvent(ev));
			};
		};

		$scope.createCampus = function(ev) {
			$scope.createCampusClicked = !$scope.createCampusClicked;

			if (!$scope.isLecturer) // "!isLecturer" Means => I Am Lecturer; if i am a lecturer (when pressing -> getting last data value before pressing)
			{
				if ($scope.user.campusMail != null) {
					validateEmail($scope.user.campusMail); // Verify the email according to "xxx@name.suffix"
				}
			}
		}

		validateEmail = function(email) {
			var result = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
			if (!result.test(email)) // TODO Fix when success to show mdDialog until 'Got it' clicked
			{
				$mdDialog.show($mdDialog.alert().title('Error - E-mail Verification').content('An error has occured in your e-mail address.')
					.ariaLabel('Email verification error alert dialog').ok('Got it!').targetEvent(email));
			}
			if (result.test(email)) // TODO Fix when success to show mdDialog until 'Got it' clicked
			{
				console.log("Im good");
				apiService.sendValidationMail(token, email).success(function(data) {
					console.log("DONE - 200");
					$mdDialog.show($mdDialog.alert().title('E-mail Verification').content('A verification e-mail has been sent to your email address.')
						.ariaLabel('Email verification alert dialog').ok('Got it!').targetEvent(email)); // Pop-up alert for e-mail verification
					$cookieStore.remove("com.sehub.www"); // Removing the cookies
					$window.location.href = 'http://se-hub.appspot.com'; // Reference to 'welcome' page
				}).error(function() {
					$mdDialog.show($mdDialog.alert().title('Error - E-mail Verification').content('An error has occured in your e-mail address or in the campus name.')
						.ariaLabel('Email verification error alert dialog').ok('Got it!').targetEvent(email));
				});
			}
		}
	}]);