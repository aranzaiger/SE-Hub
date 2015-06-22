angular.module('SeHub').controller('newTasksController', ['$scope',
	function($scope) {



		$scope.componentTypes = [{
			"type": "textbox"
		}, {
			"type": "textarea"
		}, {
			"type": "checkbox"
		}];

		$scope.task = {};
		$scope.task.task = {};
		$scope.task.components= [];
		$scope.task.isPersonal =  false;

		// $scope.task = [];

		$scope.addComponent = function() {
			$scope.task.components.push($scope.newComp);
			$scope.newComp = {};
		}

		$scope.dueTime = function(){
			if(!$scope.task.date || $scope.task.date === '')
				$scope.dueTimeFromNow =  "";
			var d = new Date($scope.task.date);
			$scope.dueTimeFromNow =  moment(d).fromNow();
		}
	}
]);