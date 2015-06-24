angular.module('SeHub')
.controller('myClassesController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.isStudent = false;
	$scope.isCourse = false;
	$scope.isNewCourse = false;
	$scope.newClassName = false;
	$scope.course = {};
	var token = $cookies['com.sehub.www'];
	$scope.user.finalDate = '';
	$scope.user.startDate = '';
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


	$scope.courses = ['SE', 'PC', 'Math', 'Calculus', 'Ivrit', 'English', 'Drugs'];


	// apiService.getClassesByUser(token).success(function(data) // Get all the campuses
	// {
	// 	$scope.courses = data;
	// }).error(function() {
	// // TODO
	// });


	$scope.chooseCourseClicked = function()
	{
		$scope.isCourse = true;
		console.log("choose course Clicked!!");
	}

	$scope.createCourseClicked = function()
	{
		$scope.isNewCourse = !$scope.isNewCourse;
	}

	$scope.submitNewClassClicked = function()
	{
	   	if($scope.course.courseName != '' && $scope.course.endDate != '' && $scope.course.startDate != '')
	    {
	    	var jsonNewCourse =
	    	{
	    		'courseName': $scope.course.courseName,
	    		'campusName': $scope.course.campusName,
	    		'startDate': {
	    			'year' : $scope.course.startDate.getFullYear(),
	    			'day' :  $scope.course.startDate.getDate(),
	    			'month': ($scope.course.startDate.getMonth() + 1)
	    		},
	    		'endDate': {
	    			'year' : $scope.course.endDate.getFullYear(),
	    			'day' :  $scope.course.endDate.getDate(),
	    			'month': ($scope.course.endDate.getMonth() + 1)
	    		}
	    	};

	    	console.log("Json here:");
    		console.log(jsonNewCourse);
	      	
	      	apiService.createCourse(token, jsonNewCourse).success(function(data)
	      	{
	      		console.log("createCourse API done");
	      	}).error(function(err)
	      	{
	      		console.log(err);
	      	});
	      	$mdDialog.show($mdDialog.alert().title('Course Created').content('You have created course successfully.')
		        .ariaLabel('Email verification alert dialog').ok('Lets Start!').targetEvent())
			.then(function() {
							$window.location.href = 'templates/views/newCourse.html'; // TODO TODO TODO
						}); // Pop-up alert

	    }
	    else
	    {
	    	$mdDialog.show($mdDialog.alert().title('Error - Creating Course').content('You have encountered and error in creating the course.')
		        .ariaLabel('Email verification alert dialog').ok('Try Again!').targetEvent());
	    }
	}



}]);