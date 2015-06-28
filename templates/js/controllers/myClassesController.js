angular.module('SeHub')
.controller('myClassesController', ['$scope', '$location', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
	function ($scope, $location, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
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
	$scope.coursesEmpty = false;
	var campusId = $routeParams.campusId;
	
	$scope.goToClass = function(classId)
	{
		console.log("Done! " + $scope.courses);
		$location.path('/projects/' + classId.toString()); // Will display all the projects in this course
	}

	$scope.chooseCourseClicked = function()
	{
		$scope.isCourse = true;
		console.log("choose course Clicked!!");

		apiService.getAllCampuses(token).success(function(data)
		{
			$scope.campuses = data;
			console.log("Campuses: " + $scope.campuses.toString());
		}).error(function(err)
		{
			console.log("Error: " + err);
		});
	}

	$scope.createCourseClicked = function()
	{
		$scope.isNewCourse = !$scope.isNewCourse;
	}

	$scope.submitNewClassClicked = function()
	{
	   	if($scope.course.courseName != null && $scope.course.endDate != null && $scope.course.startDate != null)
	    {
	    	var jsonNewCourse =
	    	{
	    		'courseName': $scope.course.courseName,
	    		'campusName': $scope.course.campusName,
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

	    	console.log("Json here: " + $scope.chosenCampus);
    		console.log(jsonNewCourse);
	      	
	      	apiService.createCourse(token, jsonNewCourse).success(function(data)
	      	{
	      		console.log("createCourse API done");
	      		$mdDialog.show($mdDialog.alert().title('Course Created').content('You have created course successfully.')
		        .ariaLabel('Email verification alert dialog').ok('Lets Start!').targetEvent())
			.then(function() {
							$location.path('/newCourse'); // TODO TODO TODO
						}); // Pop-up alert
	      	}).error(function(err)
	      	{
	      		console.log(err);
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

	//$scope.courses = ["lala", "aaa", "bbb", "ccc", "rrr"];

	var displayCourses = function()
	{
		apiService.getCourseByCampusName(token).success(function(data) // Shows all classes from this campus
		{
			$scope.courses = data;
			console.log("success " + $scope.courses);
			init(); // Executing the function to initialize course display
			if(!$scope.courses)
			{
				$scope.coursesEmpty = true;
			}
		}).error(function(err)
		{
			console.log("error: " + err);
		});		
	}


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

	displayCourses(); // Will display the courses that the user related to // TODO!!



}]);