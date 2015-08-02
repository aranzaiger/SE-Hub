angular.module('SeHub')
.controller('projectController', ['$scope', '$routeParams', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
 function ($scope, $routeParams, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
	var token = $cookies['com.sehub.www'];
	var projectId = $routeParams.projectId;
	$scope.isEditPressed = false;
	$scope.user = $scope.$parent.user;
	$scope.loadingData = true;
	$scope.displayingMessages = true;
	$scope.isMaster = false;
	$scope.isMember = false;
	$scope.project = [];
	$scope.isInProject = false;
	$scope.projectMessages = [];
	$scope.msg = {};
	$scope.isMaster = false;
	
	// $scope.thisProject = {};
	// $scope.thisProject.courseName = $routeParams.className;

	
	console.log($scope.user.id)
	// console.log($scope.projectid)

	$scope.displayProjectMessages = function()
	{
		apiService.getAllUserMessages(token).success(function(data)
	    {
	    	$scope.displayingMessages = false;
	    	// for(var i = 0; i < data.length; i ++)
	    	// 	if(!data.isPersonal)
					$scope.projectMessages = data;
	    }).error(function(err)
	    {
			console.log(err.message);
	    });
	}

	$scope.goToProfile = function(memberId)
	{
		$location.path('/profile/' + memberId);
	}
	$scope.removeUserFromProject = function()
	{
		apiService.removeUserFromProject(token, $scope.user.id, projectId).success(function(data)
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
		if($scope.user.id === $scope.project.master_id)
			$scope.isMaster = true;

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
      			$mdDialog.show($mdDialog.alert().title('Project Removal').content('Project removal failed - reason ' + err.message)
				.ariaLabel('project remove alert dialog').ok('Try Again').targetEvent(ev));
      		});
		},
		function()
		{ // No - Dont remove
		});
			// $location.path('/class/' + data.id + '/' + data.courseName); // Will display all the projects in this course
	};

	$scope.addMessageClicked = function()
	{
		$scope.addMsg = !$scope.addMsg; // Reveal the "POST" Button
	}
	$scope.postMessageClicked = function() // Posting the message itself
	{  
		if($scope.msg.msgToAdd != null)
		{
			// console.log(msg.msgToAdd);
			jsonNewMsg = {
			'groupId': parseInt(projectId), // TODO Should be ===> $scope.courseObj.id
			'message': $scope.msg.msgToAdd,
			'isProject': true
			};
			
			apiService.createMessage(token, jsonNewMsg).success(function(data)
			{
				$scope.projectMessages.push(data);
			}).error(function(err)
			{
				console.log(err.message);
			});
		}
		else
		{
			$mdDialog.show($mdDialog.alert().title('Error Creating Message').content('Message content or Course is missing')
			.ariaLabel('Send Message alert dialog').ok('Try Again!').targetEvent()); // Pop-up alert
		}
		$scope.msg.msgToAdd = null;
	}

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
			if($scope.user.id === $scope.project.master_id)
				$scope.isMaster = true;
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
	$scope.displayProjectMessages(); // Display all messages in project
	$scope.getProjectInfo(); // Get all this project data

}]);