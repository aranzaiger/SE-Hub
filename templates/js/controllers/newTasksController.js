angular.module('SeHub').controller('newTasksController', ['$scope',
	function($scope) {

		$scope.newComp = {};
		$scope.newComp.isMandatory = false;


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

		$scope.initLinkComp = function(component){
			var arr = component.label.split("|");
			for (var i = 0; i < arr.length - 1; i++) {
				if(i == 0)
					component.title = arr[i];
				else
					component.href = arr[i];
			};
		}

		$scope.initRadioButtonsComp = function(component){
			var arr = component.label.split("|");
			component.values = [];
			for (var i = 0; i < arr.length - 1; i++) {
				if(i == 0)
					component.title = arr[i];
				else
					component.values.push({text: arr[i], id: i});
			};
		}

		$scope.RB = function(comp){
			console.info(comp);
		}

	}
]);