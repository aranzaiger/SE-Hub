angular.module('SeHub')
.controller('myClassesController', ['$scope', '$location', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $location, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
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
	
	var displayCourses = function()
	{
		apiService.getCoursesByUser(token, campusId).success(function(data) // Get all the courses for display
		{
			$scope.courses = data;
			console.log("success " + $scope.courses);
			init(); // Executing the function to initialize course display
		}).error(function(err)
		{
			console.log("error: " + err);
		});
	}

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
							$window.location.href = 'templates/views/newCourse.html'; // TODO TODO TODO
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
		var i, j, counter = 0;
		var newLength = 0;
		
		if($scope.courses != null)
		{
			if(($scope.courses.length % 3) === 0)
			{
				newLength = ($scope.courses.length / 3);
			}
			else
			{
				newLength = (Math.ceil($scope.courses.length / 3)); // Rounds number up
			}
			
			console.log("length: " + newLength);
			$scope.holdArrays.length = newLength;

			for(j = 0; j < newLength; j++)	
			{
				$scope.holdArrays[j] = [3]; // Creating array in size of 3 in each array cell
			}

			for(i = 0; i < newLength; i++)		
			{		
				for(j = 0; j < newLength; j++)
				{
					if($scope.courses[(3*i) + j] != null)
					{	
						$scope.holdArrays[i][j] = $scope.courses[(3*i) + j];
					}
				}	
			}
		}
		else
		{
			$scope.coursesEmpty = true;
		}
			console.log($scope.holdArrays);
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