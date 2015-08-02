angular.module('SeHub')
	.controller('tasksController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast',
		'$mdDialog', 'apiService', '$rootScope',
		function($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService, $rootScope) {
			$scope.lecturerTasks = [];
			$rootScope.seToken = $cookies['com.sehub.www'];
			var token = $rootScope.seToken;

			$scope.user = $scope.$parent.user;
			apiService.getAllUserTasks(token).success(function(data) {
				$scope.tasks = data;
				console.log(data);
			}).error(function(err) {
				console.log(err.message);
			});


		}
	]);