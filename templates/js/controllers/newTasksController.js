angular.module('SeHub').controller('newTasksController', ['$scope',
	function($scope) {



		$scope.componentTypes = [{
			"type": "textbox"
		}, {
			"type": "textarea"
		}, {
			"type": "checkbox"
		}];



		$scope.task = [];

		$scope.addComponent = function(){
			$scope.task.push($scope.newComp);
			$scope.newComp = {};
		}
	}
]);