
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
		getUserById: function(token, id){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/users/getUserById/" + token + "/" + id;
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
		getCampusesByUser: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/campuses/getCampusesByUser/" + token;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getAllCoursesByCampus: function(token, campusId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getAllCoursesByCampus/" + token + '/' + campusId;
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
		getMessagesByGroupId: function(token, groupId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/messages/getMessagesByGroup/" + token + "/" + groupId;
			req = {
				method : "GET",
				url : url
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
		getCoursesByUser: function(token, campusId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getCoursesByUser/" + token + "/" + campusId;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getProjectsByCourse: function(token, classId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/projects/getProjectsByCourse/" + token + "/" + classId;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getProjectsById: function(token, projectId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/projects/getProjectsById/" + token + "/" + projectId;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getProjectsByUser: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/projects/getProjectsByUser/" + token;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getCampusesByUserId: function(token, id){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/campuses/getCampusesByUserID/" + token + "/" + id;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getCoursesByUserID: function(token, userId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getCoursesByUser/" + token + "/" + userId;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getAllUnsubmittedTasks: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/getAllUnsubmittedTasks/" + token;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		getAllFutureTasks: function(token, courseId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/getAllFutureTasks/" + token + "/" + courseId;
			req = {
				method : "GET",
				url : url
			};
			return $http(req);
		},
		createMessage: function(token, payLoad){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/messages/create/" + token;
			req = {
				method : "POST",
				url : url,
				data: payLoad
			};
			return $http(req);
		},
		createProject: function(token, payLoad){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/projects/create/" + token;
			req = {
				method : "POST",
				url : url,
				data: payLoad
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
		createCourse: function(token, payLoad){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/create/" + token;
			req = {
				method : "POST",
				url : url,
				data: payLoad
			};
			return $http(req);
		},
		joinCourse: function(token, courseId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/joinCourse/" + token + "/" + courseId;
			req = {
				method : "PUT",
				url : url
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
		joinProject: function(token, projectId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/projects/joinProject/" + token + "/" + projectId;
			req = {
				method: "PUT",
				url: url
			};
			return $http(req);
		},
		removeProject: function(token, projectId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/projects/deleteProject/" + token + "/" + projectId;
			req = {
				method: "DELETE",
				url: url
			};
			return $http(req);
		},
		removeUserFromProject: function(token, userId, projectId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/users/removeUserFromProject/" + token + "/" + userId + "/" + projectId;
			req = {
				method: "DELETE",
				url: url
			};
			return $http(req);
		},
		getAllFutureTasks: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/getAllFutureTasks/" + token;
			req = {
				method: "GET",
				url: url
			};
			return $http(req);
		},
		getAllUserTasks: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/getAllUserTasks/" + token;
			req = {
				method: "GET",
				url: url
			};
			return $http(req);
		},
		getAllTasksByCourse: function(token, courseId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/getAllTasksByCourse/" + token + "/" + courseId;
			req = {
				method: "GET",
				url: url
			};
			return $http(req);
		},
		getAllUserMessages: function(token){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/messages/getAllUserMessages/" + token;
			req = {
				method: "GET",
				url: url
			};
			return $http(req);
		},
		getCourseById: function(token, id){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/courses/getCoursesById/" + token + "/" + id;
			req = {
				method: "GET",
				url: url
			};
			return $http(req);
		},
		createTask: function(token, payload){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/create/" + token;
			req = {
				method: 'POST',
				data: payload,
				url: url
			};
			return $http(req);
		},
		getTaskById: function(token, taskId, ownerId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/getTaskById/" + token + "/" + taskId + "/" + ownerId;
			var req = {
				method: 'GET',
				url: url
			};
			return $http(req);

		},
		submitTask: function(token, taskId, ownerId, payload){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/submitTask/" + token + '/' + taskId + '/' + ownerId;
			req = {
				method: 'POST',
				data: payload,
				url: url
			};
			return $http(req);
		},
		submitGrade: function(token, taskId, ownerId, grade){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/submitGrade/" + token + '/' + taskId + '/' + ownerId + '/' + grade;
			req = {
				method: 'POST',
				url: url
			};
			return $http(req);
		},
		isTaskSubmitted: function(token, taskId, ownerId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/isTaskSubmitted/" + token + '/' + taskId + '/' + ownerId;
			req = {
				method: 'GET',
				url: url
			};
			return $http(req);
		},
		getUsersStateByTask: function(token, taskId){
			var url =  (DEBUG ? "http://localhost:8080" : "http://se-hub.appspot.com") + "/api/tasks/getUsersStateByTask/" + token + '/' + taskId;
			req = {
				method: 'GET',
				url: url
			};
			return $http(req);
		}
	};
}]);