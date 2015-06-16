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




	}]);