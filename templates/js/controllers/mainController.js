angular.module('SeHub')
	.controller('mainController', ['$scope', '$rootScope', 'dataService','apiService', '$cookies', '$cookieStore', '$location', '$window',

		function($scope, $rootScope, dataService, apiService, $cookies, $cookieStore, $location, $window) {
			top.setIsEnterd = true;
			var token = $cookies['com.sehub.www'];

			$scope.loadingData = true;
			$scope.isInRegisterMode = false;

			apiService.getUserByToken(token).success(function(data) {
				if (data.message == 'No User Found') {
					console.error("No User Found!");
				}
				$scope.loadingData = false;
				$scope.user = data;
				dataService.initService($scope); //Start Data Sync Service (For User)
				console.log(data);
				if ($scope.user.isFirstLogin) {
					$scope.menuObj = {};
					$scope.isInRegisterMode = true;
					$scope.loadingData = false;
					$location.path('/register')
				} else {
					$location.path('/home')
				}

			});

			

			$scope.menuItems = [{
				"title": "Dash Board",
				"icon": "fa fa-tachometer",
				"style": "selected",
				"route": "/home"
			}, {
				"title": "My Campuses",
				"icon": "fa fa-university",
				"style": "",
				"route": "/campuses"
			}, {
				"title": "My Classes",
				"icon": "fa fa-graduation-cap",
				"style": "",
				"route": "/myClasses"
			}, {
				"title": "My Projects",
				"icon": "fa fa-cube",
				"style": "",
				"route": "/campuses"
			}, {
				"title": "Tasks",
				"icon": "fa fa-clipboard",
				"style": "",
				"route": "/tasks"
			}, {
				"title": "Settings",
				"icon": "fa fa-cogs",
				"style": "",
				"route": "/Settings"
			}, {
				"title": "Log Out",
				"icon": "fa fa-power-off",
				"style": "",
				"route": "/logout"
			}];

			$scope.menuClicked = function(item) {
				var route = ""
				if (item.title == "Log Out") {
					console.info('Logging Out!');
					$cookieStore.remove('com.sehub.www');
					$window.location.href = 'http://se-hub.appspot.com'; // Reference to 'welcome' page
				}
				for (var i = $scope.menuItems.length - 1; i >= 0; i--) {
					if ($scope.menuItems[i].title === item.title) {
						$scope.menuItems[i].style = "selected";
						route = $scope.menuItems[i].route;
					} else {
						$scope.menuItems[i].style = "";
					}
				};
				top.setIsEnterd = false;
				$location.path(route);
			}


		}
	]);