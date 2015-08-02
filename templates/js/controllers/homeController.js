angular.module('SeHub')
.controller('homeController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope',
  function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
  $scope.isStudent = false;
  $scope.addMsg = false;
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
  }
  else
  {
    $scope.isStudent = true;
  }

  $scope.displayMessages = function()
  {
    apiService.getAllUserMessages(token).success(function(data)
    {
      $scope.userMessages = data;
    }).error(function(err)
    {
      console.log(err.message);
    });
  }

  $scope.addMessageClicked = function()
  {
    $scope.addMsg = !$scope.addMsg; // Reveal the "POST" Button
  }
  $scope.postMessageClicked = function() // Posting the message itself
  {
    if($scope.msg.msgToAdd != null && $scope.courseObj.courseName)
    {
      jsonNewMsg = {
      'groupId': $scope.courseObj.id, // TODO Should be ===> $scope.courseObj.id
      'message': $scope.msg.msgToAdd
      };

      apiService.createMessage(token, jsonNewMsg).success(function(data)
      {
        $scope.userMessages.push(data);
      }).error(function(err)
      {
        console.log(err.message);
      });
    }
    else
    {
      $mdDialog.show($mdDialog.alert().title('Error Creating Message').content('Message content or Course is missing')
      .ariaLabel('Send Message alert dialog').ok('Try Again!').targetEvent()); // Pop-up alert
    }
    $scope.msg.msgToAdd = null;
  }

  $scope.reviewTask = function(task)
  {
      //tasks/overview/:taskId/:submitterId/:gId', {
    if(task.isPersonal) // As Lecturer
    {
      $location.path('/tasks/overview/' + task.id + '/' + $scope.user.id + '/' + $scope.user.id);
    }
    else // it's a project task
    { 
      apiService.getProjectsByCourse(token, task.courseId).success(function(data)
      {
        for(var i = 0; i < $scope.user.projects_id_list.length; i++)
          for(var j = 0; j < data.length; j++)
            if($scope.user.projects_id_list[i] === data[j].id.toString())
              $location.path('/tasks/overview/' + task.id + '/' + data[j].id + '/' + data[j].id);
      }).error(function(err)
      {
        console.log(err.message);
      });
    }
  }

  $scope.gotoTask = function(task)
  {
    if(task.isPersonal)
    {
      $location.path('/tasks/fill/' + task.id + '/' + $scope.user.id);
    }
    else // it's a project task
    {
      apiService.getProjectsByCourse(token, task.courseId).success(function(data)
      {
        for(var i = 0; i < $scope.user.projects_id_list.length; i++)
          for(var j = 0; j < data.length; j++)
          {
            if($scope.user.projects_id_list[i] === data[j].id.toString())
            {
              $location.path('/tasks/fill/' + task.id + '/' + data[j].id);
            }
          }
      }).error(function(err)
      {
        console.log(err.message);
      });
    }
  }

  $scope.displayTasks = function()
  {
    apiService.getAllFutureTasks(token).success(function(data) // Get all Tasks // TODO change to closest TASK
    {
      $scope.userTasks = data;
    }).error(function(err)
    {
      console.log(err.message);
    });
  }

  $scope.getProjects = function(courseId)
  {
    apiService.getProjectsByCourse(token, courseId).success(function(data)
    {
      return data;
    }).error(function(err)
    {
      console.log(err.message);
    });
  }

  $scope.getCampuses = function()
  {
    apiService.getCampusesByUser(token).success(function(data)
    {
      $scope.campuses = data;
      $scope.getCourses();  // Get all the courses info
      if($scope.userMessages)
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

  $scope.chooseProjectClicked = function()
  {
    console.log("choose project Clicked!!");
  }
  
  $scope.getCampuses(); // Get all the campuses info

  // animation
  if($scope.userMessages)
  {
    $scope.displayMessages(); //  // Display all messages in message feed and the latest one
  }
  // $scope.displayMessages();
  $scope.displayTasks(); // Display all tasks in task feed and the latest one
   // $scope.getProjects(); // Get all projects info
  $scope.isEnterd = top.setIsEnterd;

}]);