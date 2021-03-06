var DEBUG = true;

var welcome = angular.module('welcome', ['ngMaterial', 'seHub.services', 'ngRoute' , 'ngCookies']);

var app = angular.module('SeHub', ['ngMaterial', 'ngRoute', 'seHub.services', 'ngCookies', 'chart.js', '720kb.datepicker']);

welcome.config(function($mdThemingProvider) {
	$mdThemingProvider.theme('default')
		.primaryPalette('teal');
});

welcome.controller('welcomeController', ['$scope', 'apiService', '$cookies', '$window', function($scope, apiService, $cookies, $window) {
	console.log("Welcome Controller");
	var uid = $cookies['com.sehub.www'];
	if(uid){
		console.info("Session in Place");
		$window.location.href = DEBUG ? 'http://localhost:8080/home' : 'http://se-hub.appspot.com/home';
	}
}]);

app.config(['$routeProvider', '$locationProvider',
	function($routeProvider, $locationProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'templates/views/home.html'
			})
			.when('/register', {
				templateUrl: 'templates/views/register.html',
				controller: 'registerController'
			})
			.when('/home', {
				templateUrl: 'templates/views/home.html',
				controller: 'homeController'
			})
			.when('/profile/:id', {
				templateUrl: 'templates/views/profile.html',
				controller: 'profileController'
			})
			.when('/tasks', {
				templateUrl: 'templates/views/tasks.html',
				controller: 'tasksController'
			})
			.when('/myClasses/:campusId', {
				templateUrl: 'templates/views/myClasses.html',
				controller: 'myClassesController'
			})
			.when('/tasks/new', {
				templateUrl: 'templates/views/newTask.html',
				controller: 'newTasksController'
			})
			.when('/tasks/overview/:taskId/:submitterId/:gId', {
				templateUrl: 'templates/views/task.html',
				controller: 'taskController'
			})
			.when('/tasks/fill/:taskId/:gId', {
				templateUrl: 'templates/views/task.html',
				controller: 'taskController'
			})
			.when('/class/:classId/:className', {
				templateUrl: 'templates/views/class.html',
				controller: 'classController'
			})
			.when('/newCourse', {
				templateUrl: 'templates/views/newCourse.html',
				controller: 'newCourseController'
			})
			.when('/campuses', {
				templateUrl: 'templates/views/campuses.html',
				controller: 'campusesController'
			})
			.when('/project/:projectId', {
				templateUrl: 'templates/views/project.html',
				controller: 'projectController'
			})
			.when('/myProjects', {
				templateUrl: 'templates/views/myProjects.html',
				controller: 'myProjectsController'
			});
	}
]);

app.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('teal')
    .accentPalette('blue-grey');

});