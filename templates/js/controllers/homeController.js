angular.module('SeHub')
.controller('homeController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
  $scope.isStudent = false;
  $scope.addMsg = false;
  $scope.msgToPost = "";
  $scope.oldText = "";
  $scope.messages = [];
  $scope.msg = {};

  $rootScope.seToken = $cookies['com.sehub.www'];
  var token = $rootScope.seToken;

  var imagePath = $scope.user.avatar_url;
  //var campusName = '';
  // $scope.campusName = '';

  $scope.phones = [
    { type: 'Home', number: '(972) 865-82861' },
    { type: 'Cell', number: '(972) 5251-32309' },
  ];



  if($scope.user.isLecturer)
  {
    $scope.isStudent = false;
    console.log("Lecturer Mode!");
    //  console.log($scope.campusName);
  }
  else
  {
    $scope.isStudent = true;
    console.log("Student Mode!");
  }

  $scope.addMessageClicked = function()
  {
    $scope.addMsg = true; // Reveal the "POST" Button
  }
  $scope.postMessageClicked = function() // Posting the message itself
  {  
    if($scope.msg.msgToAdd != null)
    {
      jsonNewMsg = {
      'courseName': 'Math', // TODO Should be ===> $scope.course.courseName
      'message': $scope.msg.msgToAdd
      };

      // console.log("J: " + jsonNewMsg.toString() + "msg: " + $scope.msg.msgToAdd);

      // apiService.createMessage(token, jsonNewMsg).success(function(data)
      // {
      //   console.log("create Msg!");
      // }).error(function(err)
      // {
      //   console.log("Error: " + err);
      // });

      /*
      'courseName': 'Advance Math',
      'message': 'The lecture today is canceled'
      */

      console.log($scope.msg.msgToAdd);
      $scope.messages.push({"text": $scope.msg.msgToAdd});
    }
    $scope.msg.msgToAdd = null;
  }

  $scope.displayTasks = function()
  {
    // apiService.getAllFutureTasks(token, courseId).success(function(data) // need to check courseId
    // {

    // }).error(function(err)
    // {

    // });


  }

  $scope.getCourses = function()
  {
    // apiService.getAllCoursesByCampus(token, campusId).success(function(data) // Shows all classes from this campus
    // {
    //   $scope.loadingData = false;
    //   $scope.courses = data;
    //   console.log("success " + $scope.courses);
    //   init(); // Executing the function to initialize course display
    //   if($scope.courses && $scope.courses.length > 0)
    //   {
    //     $scope.coursesEmpty = false;
    //   }
    // }).error(function(err)
    // {
    //   console.log("error: " + err);
    // }); 
  }

  $scope.clearAllClicked = function() // Clear Screen from text
  {
    $scope.messages = []; 
  }

  $scope.chooseCourseClicked = function()
  {
    console.log("choose course Clicked!!");
  }

  $scope.chooseProjectClicked = function()
  {
    console.log("choose project Clicked!!");
  }

  // animation
  $scope.isEnterd = top.setIsEnterd;
  $scope.getCourses(); // Get all the courses info
  $scope.displayTasks(); // Display all tasks in task feed
}]);