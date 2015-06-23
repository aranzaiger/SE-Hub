angular.module('SeHub')
.controller('myClassesController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.isStudent = false;
	$scope.isCourse = false;
	$scope.isNewCourse = false;
	$scope.newClassName = false;
	$scope.user.createNewCourse = '';
	$scope.user.finalDate = '';
	$scope.showMyClass = false;
	
	if($scope.user.isLecturer)
	{
		$scope.isStudent = false;
		console.log("Lecturer Mode!");
	}
	else
	{
		$scope.isStudent = true;
		console.log("Student Mode!");
	}


	$scope.chooseCourseClicked = function()
	{
		$scope.isCourse = true;
		console.log("choose course Clicked!!");
	}

	$scope.createCourseClicked = function()
	{
		$scope.isNewCourse = true;
		$scope.showMyClass = false;
		console.log("create course Clicked!!");
	}

	$scope.showMyCourses = function()
	{
		$scope.showMyClass = true;
		$scope.isNewCourse = false;
	}

	$scope.submitNewClassClicked = function()
	{
	   	if($scope.user.createNewCourse != '' && $scope.user.finalDate != '')
	    {
    		console.log("finalDate " + $scope.user.finalDate);
	      	console.log($scope.user.createNewCourse);
	      	$mdDialog.show($mdDialog.alert().title('Course Created').content('You have created course successfully.')
		        .ariaLabel('Email verification alert dialog').ok('Lets Start!').targetEvent());
			// $window.location.href = 'templates/views/newCourse.html'; // TODO TODO TODO
	    }
	    else
	    {
	    	$mdDialog.show($mdDialog.alert().title('Error - Creating Course').content('You have encountered and error in creating the course.')
		        .ariaLabel('Email verification alert dialog').ok('Try Again!').targetEvent());
	    }
	}



}]);