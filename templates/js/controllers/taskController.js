angular.module('SeHub')
	.controller('taskController', ['$scope', '$rootScope', 'dataService', 'apiService',
		'$cookies', '$location', '$routeParams', '$mdDialog',

		function($scope, $rootScope, dataService, apiService, $cookies, $location, $routeParams, $mdDialog) {

			var taskId = $routeParams.taskId;
			var submitterId = $routeParams.submitterId;
			var token = $cookies['com.sehub.www'];
			var groupId = $routeParams.gId;
			var user = $scope.$parent.user;
			$scope.loading = true;
			$scope.isMaster = false;

			apiService.getTaskById(token, taskId, groupId).success(function(data) {
				if(!data.grade.grade)
					data.grade.grade = 0;
				$scope.task = data;
				$scope.dateInit($scope.task.dueDate);
				apiService.getCourseById(token, data.courseId).success(function(data) {
					$scope.isMaster = (user.id === data.master_id);
				});
				if (!data.isPersonal) {
					apiService.getProjectsById(token, groupId).success(function(data) {
						$scope.group = data;
					});
				} else {
					apiService.getUserById(token, groupId).success(function(data) {
						$scope.group = data;
					});
				}
				$scope.loading = false;
			}).error(function(err) {
				$location.path('/tasks');
			})

			if (submitterId) { //In This Case we Only Want to show The Content of the Submitter
				$scope.readOnly = true;

			} else { //In This Case We Need An Empty Task To Be Able To Fill It
				$scope.readOnly = false;
			}

			$scope.dateInit = function(date) {
				d = moment(new Date(date.year, date.month - 1, date.day));
				$scope.task.date = d.format("d MMMM YYYY");
			}


			$scope.dueTime = function() {
				if (!$scope.task.date || $scope.task.date === '')
					$scope.dueTimeFromNow = "";
				var d = new Date($scope.task.date);
				$scope.dueTimeFromNow = moment(d).fromNow();
			}

			$scope.initLinkComp = function(component) {
				var arr = component.label.split("|");
				for (var i = 0; i < arr.length - 1; i++) {
					if (i == 0)
						component.title = arr[i];
					else
						component.href = arr[i];
				};
			}

			$scope.initRadioButtonsComp = function(component) {
				var arr = component.label.split("|");
				component.values = [];
				for (var i = 0; i < arr.length - 1; i++) {
					if (i == 0)
						component.title = arr[i];
					else
						component.values.push({
							text: arr[i],
							id: i
						});
				};
			}

			function validateComponents() {
				for (var i = 0; i < $scope.task.components.length; i++) {
					if ($scope.task.components[i].isMandatory && (!$scope.task.components[i].value || $scope.task.components[i].value == ''))
						return false;
				}
				return true;
			}

			$scope.submitTask = function(event) { //Dialog will pop-up if not all mandatory fields are filled
				if (validateComponents()) {
					apiService.submitTask(token, taskId, groupId, $scope.task.components).success(function(data) {
						$mdDialog.show(
							$mdDialog.alert()
							.title('Submitted!')
							.content('Your Task Was Successfully Submitted!')
							.ariaLabel('ddd')
							.ok('GoTo My Submitted Task')
							.targetEvent(event)

						).then(function() {
							$location.path('/tasks/overview/' + taskId + '/' + groupId + '/' + groupId);
						});

					})

				} else {

					$mdDialog.show(
						$mdDialog.alert()
						.title('Hey There...')
						.content('You Must Fill All Mandatory Fields In Order To Submit The Task')
						.ariaLabel('Not All Mandatory Are Filled')
						.ok('Got it!')
						.targetEvent(event)
					);
				}

			};

			$scope.submitGrade = function(event){
				apiService.submitGrade(token, taskId, groupId, $scope.task.grade.grade).success(function(data){
					$mdDialog.show(
						$mdDialog.alert()
						.title('Thanks For Grading')
						.content('The Grade was successfully posted. you can change the grade later if you want')
						.ariaLabel('Not All Mandatory Are Filled')
						.ok('Go Back To Tasks')
						.targetEvent(event)
					).then(function(){
						$location.path('/tasks');
					});
				}).error(function(err){
					$mdDialog.show(
						$mdDialog.alert()
						.title('Something Happened')
						.content('something went wrong... Try Again Later')
						.ariaLabel('Not All Mandatory Are Filled')
						.ok('No Problem!')
						.targetEvent(event)
					);
				})
			}



			$scope.dueTime = function() {
				if (!$scope.task.date || $scope.task.date === '')
					$scope.dueTimeFromNow = "";
				var d = new Date($scope.task.date);
				$scope.descriptionInit = function(desc) {
					desc.replace('\n', '<br>');
				}
				$scope.descriptionInit($scope.task.description);
				$scope.dueTimeFromNow = moment(d).fromNow();
			}

		}
	]); //End Controller