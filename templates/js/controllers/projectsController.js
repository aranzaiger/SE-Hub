angular.module('SeHub')
.controller('projectsController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	console.log("in projects controller");

	$scope.createProjectClicked = function()
	{
		console.log("project created! not rly!! ");
		// $window.location.href = 'http://localhost:8080/home#/tasks/new'; // Reference to 'newTask' page

	}

	$scope.projects = ['AMI', 'LULU', 'XIN Zhau', 'LUMI lu', 'Shimi', 'Azligi zligi', 'Drugs'];

	// apiService.getProjectsByCourse(courseId).success(function(data) // Get all the campuses
	// {
	// 	$scope.projects = data;
	// }).error(function() {
	// // TODO
	// });


}]);