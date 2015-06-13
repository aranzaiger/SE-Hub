var DEBUG = true;

var service = angular.module('seHub.services', []);

service.factory('apiService', ['$http', function($http) {


	return {
		getUserByToken: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/getUserByToken/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		getAllCampuses: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/Campuses/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		sendValidationMail: function(token, email){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/validation/sendmail/" + token;
			payload = {
				email: email
			};

			req = {
				method: "POST",
				url: url,
				data: payload
			};

			return $http(req);
		}


	};
}]);