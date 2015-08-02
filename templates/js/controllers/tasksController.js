angular.module('SeHub')
	.controller('tasksController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast',
		'$mdDialog', 'apiService', '$rootScope',
		function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope) {
			var token = $cookies['com.sehub.www'];

			$scope.user = $scope.$parent.user;
			apiService.getAllUserTasks(token).success(function(data) {
				$scope.tasks = data;

				console.log(data);
			}).error(function(err) {
				console.log(err.message);
			});


			$scope.taskClicked = function(task, classId, isPersonal) {
				var ownerId = null;
				if (classId === $scope.user.id) {
					///This Is The Lecturer
					///Need to show the List
				} else {
					if (!isPersonal) {
						apiService.getProjectsByCourse(token, task.courseId).success(function(data) {
							for (var i = 0; i < data.length; i++) {
								for (var j = 0; j < $scope.user.projects_id_list.length; j++)
									if (data[i].id.toString() === $scope.user.projects_id_list[j])
										ownerId = $scope.user.projects_id_list[j];
							}
							apiService.isTaskSubmitted(token, task.id, ownerId).success(function(data){
								if(data.submitted)
									$location.path('/tasks/overview/'+task.id+'/'+ownerId+'/'+ownerId)
								else
									$location.path('/tasks/fill/'+task.id+'/'+ownerId)
							})
						}).error(function(err) {
							console.error('Error: ', err);
						})
					}
				}
			}


		}
	]);