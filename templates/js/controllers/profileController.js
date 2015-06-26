angular.module('SeHub')
	.controller('profileController', ['$scope', '$rootScope', 'dataService', 'apiService',
		'$cookies', '$location', '$routeParams',
		function($scope, $rootScope, dataService, apiService, $cookies, $location, $routeParams) {

			var token = $cookies['com.sehub.www'];
			var id = $routeParams.id;
			$scope.loadingData = true;
			$scope.isInRegisterMode = false;

			$scope.title = "Profile";

			apiService.getUserById(token, id).success(function(data) {
				if (data.message == 'No User Found') {
					console.error("No User Found!");
				}
				$scope.user = data;
				apiService.getCampusesByUserId(token, id).success(function(data) {
					$scope.campuses = data;
					console.log(data);

					$scope.loadingData = false;
				}).error(function(err) {
					console.error(err);
				});

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
					apiService.updateUser(token, $scope.user).success(function(data) {
						console.info('User Saved');
						dataService.userBrodcast($scope.user);

					}).error(function(e) {
						console.error('Fail To Save User');
					});
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

			// $scope.campuses = [{
			// 	'title': 'JCE',
			// 	'email_ending': '@post.jce.ac.il',
			// 	'master_user_id': 123453433341,
			// 	'avatar_url': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg'
			// }, {
			// 	'title': 'Stanford',
			// 	'email_ending': '@post.jce.ac.il',
			// 	'master_user_id': 123453433341,
			// 	'avatar_url': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcR9M4uQgaJP1zyiCGw-dK31hU8buWqeuOi9vTXBd4Y8hQcFTZqA'
			// }];


			$scope.labels = ['Commits', 'Issues Assigned', 'Messages', 'Open Tasks'];
			$scope.series = ['Project A', 'Project B'];

			$scope.data = [
				[54, 3, 15, 3],
				[28, 48, 40, 3]
			];

			$scope.isUser = function() {
				return $scope.$parent.user.id.toString() /*The Actual User*/ === $routeParams.id /*The Profile User*/;
			}

		}
	]);