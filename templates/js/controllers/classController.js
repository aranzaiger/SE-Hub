angular.module('SeHub')
	.controller('classController', ['$scope', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function($scope, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope) {
		var token = $cookies['com.sehub.www'];
		var classId = $routeParams.classId;
		$scope.project = {};
		$scope.project.courseName = $routeParams.className;
		$scope.projectsEmpty = true;
		$scope.isCreateProjectClicked = false;
		$scope.submitNewCourseClicked = false;
		$scope.loadingData = true;
		$scope.isInCourse = false;
		var startDate = null;
		var endDate = null;
		var nowDate = new Date();
		var one_day=1000*60*60*24;
		var dayDeltaOfCourse;
		var courseElapseTime;
		$scope.isCourseOver = false;
		$scope.createSctionStatus = "fa fa-angle-down";

		$scope.displayProjects = function() {
			apiService.getCourseById(token, classId)
				.success(function(data) {
					startDate = new Date(data.startDate.year, data.startDate.month-1, data.startDate.day);
					endDate = new Date(data.endDate.year, data.endDate.month-1, data.endDate.day)
					$scope.course = data;
					$scope.course.startDate = startDate.toDateString();
					$scope.course.endDate = endDate.toDateString();
					dayDeltaOfCourse = (endDate.getTime() - startDate.getTime()) / one_day;
					courseElapseTime = (nowDate.getTime() - startDate.getTime()) / one_day;
					if(courseElapseTime < 0)
						courseElapseTime = 0;
					else if(courseElapseTime > dayDeltaOfCourse){
						$scope.isCourseOver = true;
						courseElapseTime = dayDeltaOfCourse;
					}
					$scope.courseTimePresentege = ((courseElapseTime/dayDeltaOfCourse) * 100).toString();
					console.log($scope.courseTimePresentege);

					apiService.getProjectsByCourse(token, classId).success(function(data) // Get all the campuses
						{
							$scope.loadingData = false;
							$scope.projects = data;
							if ($scope.projects != null && $scope.projects.length > 0) {
								$scope.projectsEmpty = false;
							}
							init(); // Executing the function to initialize projects display
							console.log("project created! not rly!! " + classId);
						}).error(function(err) {
						console.error("Error: " + err);
					});
				})
				.error(function(err) {
					console.error("Error: " + err);
				})
		}
		$scope.joinCourse = function() {
			apiService.joinCourse(token, classId).success(function(data) {
				$scope.isInCourse = true;
				$mdDialog.show($mdDialog.alert().title('Joined Course').content('You have successfully joined course.')
						.ariaLabel('Join course alert dialog').ok('Lets Start!').targetEvent())
					.then(function() {
						$location.path('/class/' + classId); // TODO TODO TODO
					}); // Pop-up alert
			}).error(function(err) {
				$mdDialog.show($mdDialog.alert().title('Error Joining Course').content(err.message + '.')
					.ariaLabel('Join course alert dialog').ok('Try Again!').targetEvent()); // Pop-up alert
				// .then(function() {
				// 				// $location.path('/newCourse'); // TODO TODO TODO
				// 			}); 
			});
		}

		$scope.createProjectClicked = function() {
			// console.log("project created! is it ?!???! " + classId);
			$scope.isCreateProjectClicked = !$scope.isCreateProjectClicked;
			if($scope.isCreateProjectClicked)
				$scope.createSctionStatus = "fa fa-angle-up";
			else
				$scope.createSctionStatus = "fa fa-angle-down";
		}

		$scope.submitNewProject = function() {
			loadingData = true;
			// debugger;
			var intClassId = parseInt(classId);
			// console.log($scope);
			var jsonNewProj = {
				'projectName': $scope.project.projectName,
				'courseId': intClassId,
				'gitRepository': $scope.project.repoOwner + '/' + $scope.project.gitRepoName
			};
			console.log(jsonNewProj);

			if ($scope.project.logoUrl)
				jsonNewProj.logo_url = $scope.project.logoUrl;

    	apiService.createProject(token, jsonNewProj).success(function(data)
    	{
    		loadingData = false;
    		projectId = data.id;
      		$mdDialog.show($mdDialog.alert().title('Project Created').content('You have successfully created project.')
	        .ariaLabel('Project created alert dialog').ok('Great!').targetEvent())
			.then(function() {
							$location.path('/project/' + projectId); // TODO TODO TODO
						}); // Pop-up alert

    	}).error(function(err)
    	{
    		console.log("Error: " + err.message);
      		$mdDialog.show($mdDialog.alert().title('Error Creating Project').content('You have failed Creating the project.')
	        .ariaLabel('Create project alert dialog').ok('Try Again!').targetEvent()); // Pop-up alert
    	});
    
	}

	$scope.goToProject = function(projectId)
	{
		console.log("projects only from classID: "  + projectId)
		$location.path('/project/' + projectId);
	}

	var init = function()
	{
		$scope.arrayHolder = [];
		var tempArr = [];
		var sizeOfSmallArrays = 3;
		for (var i = 0 ; i < $scope.projects.length ; i++) {
			if(i % sizeOfSmallArrays !== 0){
				tempArr.push($scope.projects[i]);
			}else{
				if(i !== 0){
					$scope.arrayHolder.push(tempArr);
					tempArr = [];
					tempArr.push($scope.projects[i]);
				}else{
					tempArr.push($scope.projects[i]);
				}
			}
		};
		$scope.arrayHolder.push(tempArr);
	}


	// Running...
	$scope.displayProjects(); // Displaying all projects related to user



}]);