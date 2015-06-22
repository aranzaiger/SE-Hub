angular.module('SeHub')
.controller('homeController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
  $scope.isStudent = false;
  $scope.addMsg = false;
  $scope.msgToPost = "";
  $scope.oldText = "";

  var imagePath = $scope.user.avatar_url;
  $scope.phones = [
    { type: 'Home', number: '(972) 865-82861' },
    { type: 'Cell', number: '(972) 5251-32309' },
  ];

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

  $scope.addMessageClicked = function()
  {
    $scope.addMsg = true; // Reveal the "POST" Button
  }

  $scope.postMessageClicked = function(msg) // Posting the message itself
  {  
    if(msg != null)
    {
      $scope.prevText = "- " + msg;
      implementText = document.getElementById("msg").value;
      $scope.prevText +=  "<br></br>";
      document.getElementById("bindText").innerHTML += $scope.prevText;
    }
    document.getElementById("msg").value = '';
    $scope.prevText = '';  
  }

  $scope.clearAllClicked = function() // Clear Screen from text
  {
    document.getElementById("bindText").innerHTML = "";
  }

  // animation
  $scope.isEnterd = top.setIsEnterd;
}]);