angular.module('SeHub')
.controller('projectsController', ['$scope', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	var token = $cookies['com.sehub.www'];
	var classId = $routeParams.id;
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



	$scope.displayProjects(); // Displaying all projects related to user

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
		var i, j, counter = 0;
		var newLength = 0;
		
		if(($scope.projects.length % 3) === 0)
		{
			newLength = ($scope.projects.length / 3);
		}
		else
		{
			newLength = (Math.ceil($scope.projects.length / 3)); // Rounds number up
		}
		
		console.log("length: " + newLength);
		$scope.arrayHolder.length = newLength;

		for(j = 0; j < newLength; j++)	
		{
			$scope.arrayHolder[j] = [3]; // Creating array in size of 3 in each array cell
		}

		for(i = 0; i < newLength; i++)		
		{		
			for(j = 0; j < newLength; j++)
			{
				if($scope.projects[(3*i) + j] != null)
				{	
					$scope.arrayHolder[i][j] = $scope.projects[(3*i) + j];
				}
			}	
		}
		console.log($scope.arrayHolder);
	}



	    	
	    	/*
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