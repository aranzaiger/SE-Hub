var DEBUG = true;

angular.module('seHub.services').

factory('dataService', ['$http', function($http) {
	var scope = null;


	return {
		initService: function(mainScope) {
			// this.token = user.seToken;
			// this.user = user;
			scope = mainScope;
		},
		userBrodcast: function(user) {
			scope.user = JSON.parse(JSON.stringify(user));
		}


	};
}]);