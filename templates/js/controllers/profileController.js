angular.module('SeHub')
	.controller('profileController', ['$scope', '$rootScope', 'dataService', 'apiService',
		'$cookies', '$location', '$routeParams',
		function($scope, $rootScope, dataService, apiService, $cookies, $location, $routeParams) {

			var token = $cookies['com.sehub.www'];
			var id = $routeParams.id;
			$scope.loadingData = true;
			$scope.isInRegisterMode = false;
			$scope.userExists = false;

			$scope.title = "Profile";

			apiService.getUserById(token, id).success(function(data) {
				if (!data) {
					console.error("No User Found!");
					$scope.loadingData = false;
					return;
				}
				$scope.user = data;
				$scope.userExists = true;
				apiService.getCampusesByUserId(token, id)
					.success(function(data) {
						$scope.campuses = data;
						console.log(data);
						apiService.getCoursesByUserID(token, id)
							.success(function(data) {
								$scope.courses = data;
							}).error(function(err) {
								console.error('In apiService.getCoursesByUserID', err);
							});

						$scope.loadingData = false;
					}).error(function(err) {
						console.error(err);
						console.error("++++++++++++++++++++");
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

			$scope.labels = ['Commits', 'Issues Assigned', 'Messages', 'Open Tasks'];
			//$scope.series = ['Project A', 'Project B'];

			$scope.data = [
				[54, 3, 15, 3] //,
				//[28, 48, 40, 3]
			];

			$scope.isUser = $scope.$parent.user.id.toString() /*The Actual User*/ === $routeParams.id /*The Profile User*/ ;

		}
	]);