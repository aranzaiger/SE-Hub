angular.module('SeHub')
.controller('mainController', ['$scope', '$rootScope', 'apiService', '$cookies', '$location', function ($scope, $rootScope, apiService, $cookies, $location) {

	var token = $cookies['com.sehub.www'];

	$scope.loadingData = true;
	$scope.isInRegisterMode = false;

	apiService.getUserByToken(token).success(function(data){
		if(data.message == 'No User Found'){
			console.error("No User Found!");
		}

		$scope.user = data;
		$rootScope.user = data;
		if($scope.user.isFirstLogin){
			$scope.menuObj = {};
			$scope.isInRegisterMode = true;
			$scope.loadingData = false;
			$location.path('/register')
		}
	})

	$scope.loadingData = false;

}]);