angular.module('SeHub')
.controller('thisProjectController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.isEditPressed = false;

	$scope.editPressed = function()
	{
		$scope.isEditPressed = true;
		console.log("EditPressed " + $scope.isEditPressed);
	}
	$scope.removeProject = function()
	{
		console.log("Project has been removed!");
	}

}]);