angular.module('SeHub')
.controller('mainController', ['$scope', '$rootScope', 'apiService', '$cookies', '$location', function ($scope, $rootScope, apiService, $cookies, $location) {

	$rootScope.seToken = $cookies['com.sehub.www'];
	var token = $rootScope.seToken;
	$scope.loadingData = true;

	apiService.getUserByToken(token).success(function(data){
		if(data.message == 'No User Found')
			console.error("No User Found!");

		$scope.user = data._entity;
		$rootScope.user = data._entity;
		if($scope.user.isFirstLogin)
			$location.path('/register')
	})

	$scope.loadingData = false;

}]);