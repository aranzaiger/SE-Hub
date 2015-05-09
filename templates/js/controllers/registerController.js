angular.module('SeHub')
.controller('registerController', ['$scope', '$rootScope', function ($scope, $rootScope) {
	
	$scope.userHasNoName = false;

	$scope.user = $rootScope.user;
	if($scope.user.name === ";"){
		$scope.user.name = "";
		$scope.user.name = $scope.user.username
		$scope.userHasNoName = true;
	}


}])