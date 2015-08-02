angular.module('SeHub')
.controller('projectController', ['$scope', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
 function ($scope, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	var token = $cookies['com.sehub.www'];
	var projectId = $routeParams.projectId;
	$scope.isEditPressed = false;
	$scope.user = $scope.$parent.user;
	$scope.loadingData = true;
	$scope.isMaster = false;
	$scope.isMember = false;
	$scope.project = [];
	$scope.isInProject = false;
	$scope.projectMessages = [];
	
	// $scope.thisProject = {};
	// $scope.thisProject.courseName = $routeParams.className;


	$scope.displayProjectMessages = function()
	{
		apiService.getAllUserMessages(token).success(function(data)
	    {
	      $scope.projectMessages = data;
	    }).error(function(err)
	    {
	      console.log(err.message);
	    });


	}

	$scope.goToProfile = function(memberId)
	{
		$location.path('#/profile/' + memberId);
	}
	$scope.removeUserFromProject = function()
	{
		apiService.removeUserFromProject.success(function(data)
		{

		}).error(function(err)
		{
			console.log(err.message);
		});
	}

	$scope.joinProject = function(ev)
	{
		apiService.joinProject(token, projectId).success(function(data)
		{
			$scope.isMember = true;
			$scope.project = data;
			$mdDialog.show($mdDialog.alert().title('Join Project').content('Joined successfully.')
				.ariaLabel('Join project alert dialog').ok('Aight').targetEvent(ev));
		}).error(function(err)
		{
			$mdDialog.show($mdDialog.alert().title('Join Project').content(err.message)
				.ariaLabel('Join project alert dialog').ok('Try Again').targetEvent(ev));
		});
	}

	$scope.editProject = function(ev)
	{
		$scope.isEditPressed = !$scope.isEditPressed;
	}

	$scope.removeProject = function(ev)
	{
		var confirm = $mdDialog.confirm().title('Remove Project').content('Would you like to delete this project?').ariaLabel('removeProj')
		.ok('Please do it!').cancel('No').targetEvent(ev);
		$mdDialog.show(confirm).then(function()
		{ // Yes - Remove the project
			console.log("Removed");

      		apiService.removeProject(token, projectId).success(function(data)
      		{
      			$mdDialog.show($mdDialog.alert().title('Project Removal').content('Project removed successfully.')
				.ariaLabel('project remove alert dialog').ok('Ok').targetEvent(ev));
				$location.path('/myProjects');
      		}).error(function(err)
      		{
      			$mdDialog.show($mdDialog.alert().title('Project Removal').content('Project removal failed - reason' + err.message)
				.ariaLabel('project remove alert dialog').ok('Try Again').targetEvent(ev));
      		});
		},
		function()
		{ // No - Dont remove
    		console.log("Not removed");
      
		});
			// $location.path('/class/' + data.id + '/' + data.courseName); // Will display all the projects in this course
	};

	$scope.getProfileRoute = function(userName)
	{
		for(var i = 0; i < $scope.project.members.length; i++)
		{
			if(userName === $scope.project.members[i].name)
			{
				return '#/profile/' + $scope.project.members[i].id;
			}
			else
				return '#';
		}
	}

	$scope.getProjectInfo = function()
	{
		apiService.getProjectsById(token, projectId).success(function(data)
		{
			$scope.project = data;
			for(var i = 0; i < data.members.length; i++)
			{
				if($scope.user.id === data.members[i].id)
				{
					$scope.isMember = true;
				}
			}

			apiService.getProjectsByCourse(token, $scope.project.courseId).success(function(data)
			{
				if($scope.user.projects_id_list)
					for(var i = 0; i < $scope.project.length; i++)
						if($scope.user.projects_id_list[i].id === data[i].id.toString())
							$scope.isInProject = true;
						
			}).error(function(err)
			{
				console.log(err.message);
			});

			// if($scope.user === $scope.project.info.master_id)
			// {
			// 	$scope.isMasterOrLecturer = true;
			// }
			// if($scope.project && $scope.project.length > 0) // TODO - TEST?
			// {
				$scope.loadingData = false;
			// }
		}).error(function(err)
		{
			console.log(err.message);
		});
	}
	$scope.getProjectInfo(); // Get all this project data
	$scope.displayProjectMessages(); // Display all messages in project
}]);