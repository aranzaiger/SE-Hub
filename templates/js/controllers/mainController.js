var DEBUG = true;

angular.module('SeHub')
	.controller('mainController', 
		['$scope', '$rootScope', 'dataService', 'apiService', '$cookies', 
			'$cookieStore', '$location', '$window',

		function($scope, $rootScope, dataService, apiService, $cookies, $cookieStore, $location, $window) {
			top.setIsEnterd = true;
			var token = $cookies['com.sehub.www'];

			$scope.loadingData = true;
			$scope.isInRegisterMode = false;

			apiService.getUserByToken(token).success(function(data, status) {
				if (status == 204) {
					console.error("No User Found!");
					$cookieStore.remove('com.sehub.www');
					window.location = DEBUG ? 'http://localhost:8080' : 'http://se-hub.appstpot.com/';
				}
				$scope.loadingData = false;
				$scope.user = data;

				$scope.menuItems = [{
					"title": "Dash Board",
					"icon": "fa fa-tachometer",
					"style": "selected",
					"route": "/home"
				},  {
					"title": "Explore",
					"icon": "fa fa-compass",
					"style": "",
					"route": "/campuses"
				}, {
					"title": "My Projects",
					"icon": "fa fa-cube",
					"style": "",
					"route": "/myProjects"
				}, {
					"title": "Tasks",
					"icon": "fa fa-clipboard",
					"style": "",
					"route": "/tasks"
				}, {
					"title": "Profile",
					"icon": "fa fa-cogs",
					"style": "",
					"route": "/profile/" + $scope.user.id.toString()
				}, {
					"title": "Log Out",
					"icon": "fa fa-power-off",
					"style": "",
					"route": "/logout"
				}];

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

			}).error(function(err){
				console.error(err);
				$cookieStore.remove('com.sehub.www');
				window.location = DEBUG ? 'http://localhost:8080' : 'http://se-hub.appstpot.com/';
			});



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