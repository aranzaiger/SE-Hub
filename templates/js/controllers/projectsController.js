angular.module('SeHub')
.controller('projectsController', ['$scope', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	var token = $cookies['com.sehub.www'];
	var classId = $routeParams.classId;
	$scope.projectEmpty = false;

	$scope.displayProjects = function()
	{
		console.log("in displayProjecs!!! ");
		apiService.getProjectsByCourse(token, classId).success(function(data) // Get all the campuses
		{
			$scope.projects = data;
			init(); // Executing the function to initialize projects display
			console.log("project created! not rly!! " + classId);
		}).error(function(err)
		{
			console.log("Error: " + err);
		});
		if($scope.projects = null)
		{
			$scope.projectEmpty = true;
		}
	}
	$scope.joinCourse = function()
	{
		apiService.joinCourse(token, classId).success(function(data)
		{
			console.log("Success!!");
      		$mdDialog.show($mdDialog.alert().title('Joined Course').content('You have successfully joined course.')
	        .ariaLabel('Join course alert dialog').ok('Lets Start!').targetEvent())
			.then(function() {
							$location.path('/projects/' + classId); // TODO TODO TODO
						}); // Pop-up alert
		}).error(function(err)
		{
      		$mdDialog.show($mdDialog.alert().title('Error Joining Course').content('You have failed joined the course.')
	        .ariaLabel('Join course alert dialog').ok('Try Again!').targetEvent()); // Pop-up alert
			// .then(function() {
			// 				// $location.path('/newCourse'); // TODO TODO TODO
			// 			}); 
		});
	}

	$scope.createProjectClicked = function()
	{
		console.log("project created! not rly!! " + classId);
		
		// $window.location.href = 'http://localhost:8080/home#/tasks/new'; // Reference to 'newTask' page
	}

	// $scope.projects = ['AMI', 'LULU', 'XIN Zhau', 'LUMI lu', 'Shimi', 'Azligi zligi', 'Drugs'];

	$scope.goToProject = function()
	{
		console.log("projects only from classID: "  + classId)
		$location.path('/thisProject' + classId);
	}

	var init = function()
	{
		$scope.arrayHolder = [];
		var tempArr = [];
		var sizeOfSmallArrays = 3;
		for (var i = 0 ; i < $scope.courses.length ; i++) {
			if(i % sizeOfSmallArrays !== 0){
				tempArr.push($scope.courses[i]);
			}else{
				if(i !== 0){
					$scope.arrayHolder.push(tempArr);
					tempArr = [];
					tempArr.push($scope.courses[i]);
				}else{
					tempArr.push($scope.courses[i]);
				}
			}
		};
		$scope.arrayHolder.push(tempArr);
	}


	// Running...
	$scope.displayProjects(); // Displaying all projects related to user


	    	
	    	/*
	    	var jsonNewCourse =
	    	{
	    		'projectName': $scope.course.courseName,
	    		'courseId': classId,
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
	    	};*/

	    		/*
			{
		'projectName': 'Advance Math',
		'courseName': 'JCE',
		'grade': 98,
		'logo_url': 'http://location.domain.com/image.jpg',
		'gitRepository': 'http://location.git.com/somthing',
		'membersId': ['bob', 'dylan', 'quentin', 'terentino'],
		'id' : 1234567890
		} 
	*/






}]);