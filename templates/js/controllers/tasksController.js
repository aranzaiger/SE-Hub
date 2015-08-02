angular.module('SeHub')
	.controller('tasksController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast',
		'$mdDialog', 'apiService', '$rootScope',
		function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope) {
			var token = $cookies['com.sehub.www'];

			$scope.user = $scope.$parent.user;
			apiService.getAllUserTasks(token).success(function(data) {
				$scope.tasks = data;
			}).error(function(err) {
				console.error(err.message);
			});


			$scope.taskClicked = function(task, classId, isPersonal, masterId, ev) {
				var ownerId = null;
				if (masterId === $scope.user.id) {
					///This Is The Lecturer
					///Need to show the List
					$mdDialog.show({
							controller: DialogController,
							templateUrl: 'templates/views/UserStateList.html?v=1122231',
							parent: $scope,
							targetEvent: ev,
							locals: {
								data: {
									task: task,
									token: token,
									isPersonal: isPersonal
								}
							}
						})
						.then(function(answer) {
							$scope.alert = 'You said the information was "' + answer + '".';
						}, function() {
							$scope.alert = 'You cancelled the dialog.';
						});


				} else {
					if (!isPersonal) {
						apiService.getProjectsByCourse(token, task.courseId).success(function(data) {
							for (var i = 0; i < data.length; i++) {
								for (var j = 0; j < $scope.user.projects_id_list.length; j++)
									if (data[i].id.toString() === $scope.user.projects_id_list[j])
										ownerId = $scope.user.projects_id_list[j];
							}
							apiService.isTaskSubmitted(token, task.id, ownerId).success(function(data) {
								if (data.submitted) {
									if (ownerId)
										$location.path('/tasks/overview/' + task.id + '/' + ownerId + '/' + ownerId);
									else {
										$mdDialog.show(
											$mdDialog.alert()
											.title('You Have No Project in this class')
											.content('To Be Able To Fill A Project Task you need to be assigned to a project')
											.ariaLabel('ddd')
											.ok('Ok, ill join/create a project')
											.targetEvent(event)

										).then(function() {
											$location.path('/campuses');
										});
									}
								} else {
									if (ownerId)
										$location.path('/tasks/fill/' + task.id + '/' + ownerId);
									else {
										$mdDialog.show(
											$mdDialog.alert()
											.title('You Have No Project in this class')
											.content('To Be Able To Fill A Project Task you need to be assigned to a project')
											.ariaLabel('ddd')
											.ok('Ok, ill join/create a project')
											.targetEvent(event)

										).then(function() {
											$location.path('/campuses');
										});
									}
								}
							}).error(function(err) {
								console.error(err);
							});
						}).error(function(err) {
							console.error('Error: ', err);
						});
					} else {
						apiService.isTaskSubmitted(token, task.id, $scope.user.id).success(function(data) {
							if (data.submitted) {
								$location.path('/tasks/overview/' + task.id + '/' + $scope.user.id + '/' + $scope.user.id);
							} else {
								$location.path('/tasks/fill/' + task.id + '/' + $scope.user.id);
							}
						}).error(function(err) {
							console.error(err);
						})
					}
				}
			}

			$scope.createNewTask = function() {
				$location.path('/tasks/new');
			}


			function DialogController($scope, $mdDialog, data, apiService) {
				$scope.task = data.task;
				$scope.isPersonal = data.isPersonal;
				var token = data.token;
				$scope.loading = true;

				apiService.getUsersStateByTask(token, $scope.task.id).success(function(data) {
					$scope.classList = data;
					$scope.loading = false;
				}).error(function(err) {
					console.error(err);
					$scope.hide();
				})

				$scope.goToTask = function(obj) {
					$mdDialog.hide();
					$location.path('/tasks/overview/' + $scope.task.id + '/' + obj.id + '/' + obj.id);
				}


				$scope.hide = function() {
					$mdDialog.hide();
				};
				$scope.cancel = function() {
					$mdDialog.cancel();
				};
				$scope.answer = function(answer) {
					$mdDialog.hide(answer);
				};
			}



		}
	]);