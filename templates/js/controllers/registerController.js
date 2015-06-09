angular.module('SeHub')
.controller('registerController', ['$scope', '$rootScope', function ($scope, $rootScope) {
	
	$scope.userHasNoName = false;

	$scope.user = $rootScope.user;
	if($scope.user.name === ";"){
		$scope.user.name = "";
		$scope.user.name = $scope.user.username
		$scope.userHasNoName = true;
	}

	///TESTING
	$scope.campuses = [
		{															
			title: 'JCE',
			capus_avatar: "http://asdasfa.asdasd.com/img.jpg"
		},
		{
			title: 'JCE1',
			capus_avatar: "http://asdasfa.asdasd.com/img.jpg"
		},
		{
			title: "JCE2",
			capus_avatar: "http://asdasfa.asdasd.com/img.jpg"
		}
	];


}]);																						