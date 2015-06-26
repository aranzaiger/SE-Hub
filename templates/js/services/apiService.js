
var DEBUG = true;

var service = angular.module('seHub.services', []);

service.factory('apiService', ['$http', function($http) {
	return {
		getUserByToken: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/users/getUserByToken/" + token;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getAllCampuses: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/campuses/getAll/" + token;
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
		},
		updateUser: function(token, payLoad){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/users/updateUser/" + token;
			
			req = {
				method: "PUT",
				url: url,
				data: payLoad
			};
			return $http(req);
		},
		getCourseByCampusName: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getAll/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		getAllCourses: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getAll/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		getAllMessages: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getAllMessages/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		createMessage: function(token, payLoad){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/createMessage/" + token;
			req = {
				method : "POST",
				url : url,
				data: payLoad

			};
			return $http(req);
		},
		getMessagesByCourseName: function(token, courseName){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getMessagesByCourseName/" + token + '/' + courseName;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		createCourse: function(token, payLoad){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/create/" + token;
			req = {
				method : "POST",
				url : url,
				data: payLoad

			};
			return $http(req);
		},
		getCampusesByUser: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/campuses/getCampusesByUser/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		getClassesByCourse: function(){ // Need to add camusName (ngRoute) ~ sagi //TODO
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/ClassesByCourse/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		},
		getProjectsByCourse: function(){ // Need to add courseID (ngRoute) ~ sagi //TODO
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getProjectByCourse/" + token;
			req = {
				method : "GET",
				url : url

			};
			return $http(req);
		}
	};
}]);