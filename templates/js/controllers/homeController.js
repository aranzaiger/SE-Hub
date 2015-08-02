angular.module('SeHub')
.controller('homeController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
  function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
  $scope.isStudent = false;
  $scope.addMsg = false;
  $scope.msgToPost = "";
  $scope.oldText = "";
  $scope.messages = [];
  $scope.userMessages = [];
  $scope.userTasks = [];
  $scope.messagesDisplay = [];
  $scope.courses = [];
  $scope.campuses = [];
  $scope.msg = {};
  $scope.courseObj = {};
  $scope.user = $scope.$parent.user;
  $rootScope.seToken = $cookies['com.sehub.www'];
  var token = $rootScope.seToken;

  if($scope.user.isLecturer)
  {
    $scope.isStudent = false;
    console.log("Lecturer Mode!");
  }
  else
  {
    $scope.isStudent = true;
    console.log("Student Mode!");
  }

  $scope.displayMessages = function()
  {
    apiService.getAllUserMessages(token).success(function(data)
    {
      // console.log(data);
      $scope.userMessages = data;
    }).error(function(err)
    {
      console.log("Error: " + err.message);
    });
  }

  // $scope.displayMessages(); //

  $scope.addMessageClicked = function()
  {
    $scope.addMsg = true; // Reveal the "POST" Button
  }
  $scope.postMessageClicked = function() // Posting the message itself
  {  
    console.log($scope.courseObj);
    if($scope.msg.msgToAdd != null && $scope.courseObj.courseName)
    {
      console.log("NOW");

      jsonNewMsg = {
      'groupId': $scope.courseObj.id, // TODO Should be ===> $scope.courseObj.id
      'message': $scope.msg.msgToAdd
      };

      apiService.createMessage(token, jsonNewMsg).success(function(data)
      {
        console.log("create Msg!");
      }).error(function(err)
      {
        console.log("Error Below");
        console.log(err.message);
      });

      $scope.userMessages.push({"text": $scope.msg.msgToAdd});
      $location.path('/home/');
    }
    else
    {
      $mdDialog.show($mdDialog.alert().title('Error Creating Message').content('Message content or Course is missing')
      .ariaLabel('Send Message alert dialog').ok('Try Again!').targetEvent()); // Pop-up alert
    }
    $scope.msg.msgToAdd = null;
  }

  $scope.displayTasks = function()
  {
    apiService.getAllFutureTasks(token).success(function(data) // Get all Tasks // TODO change to closest TASK
    {
      $scope.userTasks = data;
      console.log(data);
    }).error(function(err)
    {
      console.log(err.message);
    });

    // apiService.getAllFutureTasks(token, courseId).success(function(data) // need to check courseId
    // {
    //   console.log("YE");
    // }).error(function(err)
    // {
    //   console.log("Error: " + err.message);
    // });

  }

  $scope.getCampuses = function()
  {
    apiService.getCampusesByUser(token).success(function(data)
    {
      $scope.campuses = data;
      $scope.getCourses();  // Get all the courses info
      if($scope.messages)
      {
        //$scope.displayMessages(); //  // Display all messages in message feed and the latest one
      }
    }).error(function(err)
    {
      console.log(err.message);
    });

  }

  $scope.getCourses = function()
  {
    for(var i = 0; i < $scope.campuses.length; i++) 
    {
      apiService.getAllCoursesByCampus(token, $scope.campuses[i].id).success(function(data) // Shows all classes from this campus
      {
        $scope.loadingData = false;
        $scope.courses = data;
        // console.log($scope.courses);
        if($scope.courses && $scope.courses.length > 0)
        {
          $scope.coursesEmpty = false;
        }
      }).error(function(err)
      {
        console.log("Error: " + err.message);
      }); 
     }
  }

  $scope.clearAllClicked = function() // Clear Screen from text
  {
    $scope.userMessages = []; 
  }

  $scope.chooseCourseClicked = function()
  {
    // console.log($scope.courseObj);
    if($scope.courseObj)
    {
      for(var i = 0; i < $scope.courses.length; i++)
      {
        if($scope.courses[i].courseName === $scope.courseObj.name)
        {
          $scope.courseObj = $scope.courses[i];
        }
      }
    }
    console.log($scope.courseObj);
  }

  // $scope.chooseCourseClicked = function()
  // {
  //   console.log("Click ");
  //   console.log($scope.choosenCourse);
  //   if($scope.choosenCourse)
  //   {
  //     console.log("here");
  //     $scope.courseObj = null;
  //     for(var i = 0; i < $scope.courses.length; i++)
  //     {
  //       if($scope.courses[i].courseName === $scope.choosenCourse)
  //       {
  //         $scope.courseObj = $scope.courses[i];
  //         console.log($scope.courseObj);
  //       }
  //     }
  //   }
  // }

  $scope.chooseProjectClicked = function()
  {
    console.log("choose project Clicked!!");
  }
  
  $scope.getCampuses(); // Get all the campuses info

  // animation
  $scope.displayMessages();
  $scope.displayTasks(); // Display all tasks in task feed and the latest one
  $scope.isEnterd = top.setIsEnterd;

}]);