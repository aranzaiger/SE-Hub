angular.module('SeHub')
.controller('newCourseController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{

	$scope.goBack = function()
	{
		$window.location.href = 'templates/views/myClasses.html';
	}

}]);