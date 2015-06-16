angular.module('SeHub')
	.controller('mainController', ['$scope', '$rootScope', 'apiService', '$cookies', '$location', function($scope, $rootScope, apiService, $cookies, $location) {

		var token = $cookies['com.sehub.www'];

		$scope.loadingData = true;
		$scope.isInRegisterMode = false;

		apiService.getUserByToken(token).success(function(data) {
			if (data.message == 'No User Found') {
				console.error("No User Found!");
			}

			$scope.user = data;
			if ($scope.user.isFirstLogin) {
				$scope.menuObj = {};
				$scope.isInRegisterMode = true;
				$scope.loadingData = false;
				$location.path('/register')
			} else {
				$location.path('/home')
			}

		})

		apiService.getUserByToken(token).success(function(data) // Get user token
			{
				$scope.user = data;
				$scope.loadingData = false;

				apiService.getAllCampuses($scope.user.seToken).success(function(data) // Get all the campuses
					{
						$scope.campuses = data;
					}).error(function() {

				});
			});

		$scope.menuItems = [{
			"title": "Home",
			"icon": "fa fa-home",
			"style": "selected",
			"route": "#/home"
		}, {
			"title": "My Campuses",
			"icon": "fa fa-university",
			"style": "",
			"route": "/campuses"
		}, {
			"title": "My Classes",
			"icon": "fa fa-graduation-cap",
			"style": "",
			"route": "/campuses"
		}, {
			"title": "My Projects",
			"icon": "fa fa-cube",
			"style": "",
			"route": "/campuses"
		}, {
			"title": "Tasks",
			"icon": "fa fa-clipboard",
			"style": "",
			"route": "/campuses"
		}, {
			"title": "Settings",
			"icon": "fa fa-cogs",
			"style": "",
			"route": "#/Settings"
		}, {
			"title": "Log Out",
			"icon": "fa fa-power-off",
			"style": "",
			"route": "#/logout"
		}];

	}]);