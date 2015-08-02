angular.module('SeHub').controller('newTasksController', ['$scope', 'apiService', '$cookies', '$location' ,
	function($scope, apiService, $cookies, $location) {

		$scope.newComp = {};
		$scope.newComp.isMandatory = false;
		var user = $scope.$parent.user;
		var token = $cookies['com.sehub.www'];
		$scope.submitting = false;
		$scope.course = {}
		$scope.loading = true;
		apiService.getCoursesByUserID(token, user.id.toString()).success(function(data) {
			$scope.courses = [];
			for (var i = 0; i < data.length; i++) {
				if (data[i].master_id == user.id)
					$scope.courses.push(data[i]);
			}
			$scope.loading = false;
		}).error(function(err) {
			console.error('Error', err);
			$scope.courses = [];
			$scope.loading = false;
		});

		var compOrder = 0;


		$scope.courseSelected = function() {
			for (var i = 0; i < $scope.courses.length; i++) {
				if ($scope.course.title === $scope.courses[i].courseName) {
					$scope.course.id = $scope.courses[i].id;
					$scope.task.courseId = $scope.course.id;
				}
			}
		};

		$scope.submit = function() {
			if (validForm()) {
				$scope.submitting = true;
				var payload = $scope.task;
				payload.dueDate = new Date(payload.date);
				payload.dueDate = {
					year: payload.dueDate.getFullYear(),
					month: payload.dueDate.getMonth() + 1,
					day: payload.dueDate.getDate()

				}
				
				apiService.createTask(token, payload).success(function(data){
					$location.path('/tasks');
				}).error(function(err){
					console.error(err);
				})
			} else {
				alert('Fill All Shit!');
			}
		}

		function validForm() {
			if (!$scope.course.title)
				return false;
			if (!$scope.task.title || $scope.task.title.trim() == '')
				return false;
			if (!$scope.task.description || $scope.task.description.trim() == '')
				return false;
			if (!$scope.task.date)
				return false;

			return true;
		}


		$scope.componentTypes = [{
			"type": "textbox"
		}, {
			"type": "textarea"
		}, {
			"type": "checkbox"
		}, {
			"type": "link"
		}, {
			"type": "radiobuttons"
		}];

		$scope.task = {};
		$scope.task.task = {};
		$scope.task.components = [];
		$scope.task.isPersonal = false;

		// $scope.task = [];

		$scope.addComponent = function() {
			var comp = {};
			var type = $scope.newComp.type;
			comp.type = type;
			comp.order = compOrder;
			compOrder ++;
			comp.isMandatory = $scope.newComp.isMandatory;
			comp.label = "";
			var i = 0
			if (!(type === 'textbox' || type === 'textarea' || type === 'checkbox'))
				while ($scope.newComp.label[i]) {
					comp.label += $scope.newComp.label[i] + "|";
					i++;
				} else
					comp.label = $scope.newComp.label[i];

			console.log(comp);
			$scope.task.components.push(comp);

			// console.log($scope.newComp);
			$scope.newComp = {};
			$scope.newComp.isMandatory = false;
			$scope.compDetails = [];
			$scope.isRadioButton = false;

		}

		$scope.ComponentType = function(type) {
			if (type === 'textbox' || type === 'textarea' || type === 'checkbox')
				$scope.compDetails = [{
					detail: "Label"
				}];
			else if (type === 'radiobuttons') {
				$scope.compDetails = [{
					detail: "Label"
				}];
				$scope.compDetails.push({
					detail: "Option" + $scope.compDetails.length + ": "
				});
			} else if (type === 'link')
				$scope.compDetails = [{
					detail: "Label"
				}, {
					detail: "URL Path"
				}];

			if (type === 'radiobuttons')
				$scope.isRadioButton = true;
			else
				$scope.isRadioButton = false;
		}

		$scope.addMoreOptions = function() {
			$scope.compDetails.push({
				detail: "Option" + $scope.compDetails.length + ": "
			});
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

		$scope.RB = function(comp) {
			console.info(comp);
		}

	}
]);