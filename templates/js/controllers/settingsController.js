angular.module('SeHub')
	.controller('settingsController', ['$scope', '$rootScope', 'dataService', 'apiService', '$cookies', '$location',
		function($scope, $rootScope, dataService, apiService, $cookies, $location) {

			var token = $cookies['com.sehub.www'];

			$scope.loadingData = true;
			$scope.isInRegisterMode = false;

			$scope.title = "Settings"

			apiService.getUserByToken(token).success(function(data) {
				if (data.message == 'No User Found') {
					console.error("No User Found!");
				}
				$scope.loadingData = false;
				$scope.user = data;
				console.log(data);
				if ($scope.user.isFirstLogin) {
					$scope.menuObj = {};
					$scope.isInRegisterMode = true;
					$scope.loadingData = false;
					$location.path('/register')
				}

			});

			$scope.isEditMode = false;
			$scope.profileMode = "Edit Profile";
			$scope.profileModeIcon = "fa fa-pencil";

			$scope.changeProfileMode = function() {
				$scope.isEditMode = !$scope.isEditMode;
				if ($scope.isEditMode) {
					$scope.profileMode = "Save Profile";
					$scope.profileModeIcon = "fa fa-floppy-o";
				} else {
					dataService.userBrodcast($scope.user);
					$scope.profileMode = "Edit Profile";
					$scope.profileModeIcon = "fa fa-pencil";
				}
			}

			/**
			 * DEBUG DATA
			 */
			$scope.courses = [{
				"courseName": "Advance Math",
				"campusName": "JCE",
				"startDate": {
					"year": 2015,
					"month": 4,
					"day": 3
				},
				"endDate": {
					"year": 2016,
					"month": 5,
					"day": 14
				},
				"taskFlag": false,
				"campus_avatar": "https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg"
			}];

			$scope.campuses = [{
				'title': 'JCE',
				'email_ending': '@post.jce.ac.il',
				'master_user_id': 123453433341,
				'avatar_url': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg'
			}, {
				'title': 'Stanford',
				'email_ending': '@post.jce.ac.il',
				'master_user_id': 123453433341,
				'avatar_url': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcR9M4uQgaJP1zyiCGw-dK31hU8buWqeuOi9vTXBd4Y8hQcFTZqA'
			}];


		}
	]);