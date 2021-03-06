angular.module('SeHub')
.controller('myClassesController', ['$scope', '$location', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
	function ($scope, $location, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	$scope.loadingData = true;
	$scope.isStudent = false;
	$scope.isCourse = false;
	$scope.isNewCourse = false;
	$scope.newClassName = false;
	$scope.course = {};
	var token = $cookies['com.sehub.www'];
	$scope.user.finalDate = '';
	$scope.user.startDate = '';
	$scope.showMyClass = false;
	$scope.coursesEmpty = true;
	$scope.campusId;
	$scope.isMemberInCourse = false;
	var campusId = $routeParams.campusId;
	
	$scope.goToClass = function(classId, className)
	{
		$location.path('/class/' + classId.toString() + '/' + className); // Will display all the projects in this course
	}

	$scope.chooseCampusClicked = function()
	{
		$scope.isCourse = true;

		apiService.getAllCampuses(token).success(function(data)
		{
			$scope.campuses = data;
		}).error(function(err)
		{
			console.log(err.message);
		});
	}

	$scope.createCourseClicked = function()
	{
		$scope.isNewCourse = !$scope.isNewCourse;
	}

	$scope.submitNewClassClicked = function()
	{
		var i;
	   	if($scope.course.courseName != null && $scope.course.endDate != null && $scope.course.startDate != null)
	    {
		 	for(i = 0; i < $scope.campuses.length; i++)   	
			{		    	
		    	if($scope.course.campusName === $scope.campuses[i].title)
		    	{
		    		$scope.campusId = $scope.campuses[i].id;
		    	}
		    }

	    	var jsonNewCourse =
	    	{
	    		'courseName': $scope.course.courseName,
	    		'campusId': $scope.campusId,
	    		'startDate': {
	    			'year' : $scope.course.startDate.getFullYear(),
	    			'day' : $scope.course.startDate.getDate(),
	    			'month': $scope.course.startDate.getMonth() + 1
	    		},
	    		'endDate': {
	    			'year' : $scope.course.endDate.getFullYear(),
	    			'day' : $scope.course.endDate.getDate(),
	    			'month': $scope.course.endDate.getMonth() + 1
	    		}
	    	};

	      	
	      	apiService.createCourse(token, jsonNewCourse).success(function(data)
	      	{
	      		$mdDialog.show($mdDialog.alert().title('Course Created').content('You have created course successfully.')
		        .ariaLabel('Email verification alert dialog').ok('Lets Start!').targetEvent())
			.then(function() {
							$location.path('/class/' + data.id + '/' + data.courseName); // Will display all the projects in this course
						}); // Pop-up alert
	      	}).error(function(err)
	      	{
	      		$mdDialog.show($mdDialog.alert().title('Error Creating Class').content(err)
	      		.ariaLabel('Create Class alert dialog').ok('Try Again!').targetEvent()); // Pop-up alert
	      	});
	    }
	    else
	    {
	    	$mdDialog.show($mdDialog.alert().title('Error - Creating Course').content('Some fields are missing.')
		        .ariaLabel('Email verification alert dialog').ok('Try Again!').targetEvent());
	    }
	}

	var init = function()
	{
		$scope.holdArrays = [];
		var tempArr = [];
		var sizeOfSmallArrays = 3;
		for (var i = 0 ; i < $scope.courses.length ; i++) {
			if(i % sizeOfSmallArrays !== 0){
				tempArr.push($scope.courses[i]);
			}else{
				if(i !== 0){
					$scope.holdArrays.push(tempArr);
					tempArr = [];
					tempArr.push($scope.courses[i]);
				}else{
					tempArr.push($scope.courses[i]);
				}
			}
		};
		$scope.holdArrays.push(tempArr);
	}

	var displayCourses = function()
	{
		apiService.getAllCoursesByCampus(token, campusId).success(function(data) // Shows all classes from this campus
		{
			$scope.loadingData = false;
			$scope.courses = data;
			init(); // Executing the function to initialize course display
			if($scope.courses && $scope.courses.length > 0)
			{
				$scope.coursesEmpty = false;
			}
		}).error(function(err)
		{
			console.log(err.message);
		});		
	}

	if($scope.user.isLecturer)
	{
		$scope.isStudent = false;
	}
	else
	{
		$scope.isStudent = true;
	}
	displayCourses(); // Will display the courses that the user related to // TODO!!
}]);