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
  $scope.course = '';
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

  // apiService.getCourseByCampusName($scope.user.classes_id_list[0]).success(function(data)
  // {
  //   console.log("Campus Name is ON! " + $scope.user.classes_id_list[0])
  //   $scope.course = data;
  // }).error(function()
  // {
  //   console.log("Error on ===> getCourseByCampusName")
  // });


  $scope.addMessageClicked = function()
  {
    $scope.addMsg = true; // Reveal the "POST" Button
  }
  $scope.postMessageClicked = function() // Posting the message itself
  {  
    if($scope.msg.msgToAdd != null)
    {
      console.log($scope.msg.msgToAdd);
      $scope.messages.push({"text": $scope.msg.msgToAdd});
    }
    $scope.msg.msgToAdd = null;
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
}]);