angular.module('SeHub')
	.controller('taskController', ['$scope', '$rootScope', 'dataService', 'apiService',
		'$cookies', '$location', '$routeParams', '$mdDialog',

		function($scope, $rootScope, dataService, apiService, $cookies, $location, $routeParams, $mdDialog) {

			var taskId = $routeParams.taskId;
			var submitterId = $routeParams.submitterId;
			var token = $cookies['com.sehub.www'];
			var groupId = $routeParams.gId;

			apiService.getTaskById(token, taskId, groupId).success(function(data){
				$scope.task = data;
				$scope.dateInit($scope.task.dueDate);
			}).error(function(err){
				console.error('Error: ', err);
			})

			if (submitterId) { //In This Case we Only Want to show The Content of the Submitter
				$scope.readOnly = true;

			} else { //In This Case We Need An Empty Task To Be Able To Fill It
				$scope.readOnly = false;
				apiService.getTaskById(token, taskId, groupId);
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
					alert('All Shit Are Filled');
					return;
				}
				$mdDialog.show(
					$mdDialog.alert()
					.title('Hey There...')
					.content('You Must Fill All Mandatory Fields In Order To Submit The Task')
					.ariaLabel('Not All Mandatory Are Filled')
					.ok('Got it!')
					.targetEvent(event)
				);

			}



			/*=================================
			=            Mock Data            =
			=================================*/

			// $scope.task = {
			// 	"title": "task1",
			// 	"courseId": 1234567890,
			// 	"description": "one line\nsecondline\nthirdline",
			// 	"dueDate": {
			// 		"year": 2010,
			// 		"month": 2,
			// 		"day": 4
			// 	},
			// 	"isPersonal": true,
			// 	"components": [{
			// 		"type": "radiobuttons",
			// 		"label": "pick One|this|orthis|MaybeThis",
			// 		"isMandatory": true,
			// 		"order": 1
			// 	}, {
			// 		"type": "checkbox",
			// 		"label": "tick Me",
			// 		"isMandatory": true,
			// 		"order": 2
			// 	}, {
			// 		"type": "textarea",
			// 		"label": "fill shit",
			// 		"isMandatory": false,
			// 		"order": 3
			// 	}]
			// };

			

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