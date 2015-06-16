angular.module('SeHub')
	.controller('settingsController', ['$scope', '$rootScope', 'apiService', '$cookies', '$location', function($scope, $rootScope, apiService, $cookies, $location) {

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
				$scope.profileMode = "Edit Profile";
				$scope.profileModeIcon = "fa fa-pencil";
			}
		}

		// {
		// name: ";"
		// isLecturer: false
		// email: "sagidayan@gmail.com"
		// username: "sagidayan"
		// seToken: "76cd4178-94dd-4cb4-b464-111d2239e567"
		// isFirstLogin: true
		// campuses_id_list: [0]
		// classes_id_list: [0]
		// avatar_url: "https://avatars.githubusercontent.com/u/2984053?v=3"
		// }


	}]);