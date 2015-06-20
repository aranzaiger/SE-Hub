angular.module('SeHub')
.controller('homeController', ['$scope', '$cookies', '$cookieStore', '$window', '$location', '$mdToast', '$mdDialog', 'apiService', '$rootScope', function ($scope, $cookies, $cookieStore, $window, $location, $mdToast, $mdDialog, apiService ,$rootScope)
{
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
    console.log("Lecturer Mode!");
    $scope.messages = [
      {
        face : imagePath,
        what: 'Let me tell you a secret',
        who: 'Sagi Dayan',
        when: '4:15PM',
        notes: " I am S'ein"
      },
      {
        face : imagePath,
        what: 'Listen to this!',
        who: 'Aran Zaiger',
        when: '6:15PM',
        notes: " I am gaylord ultima!!"
      },
      {
        face : imagePath,
        what: 'Hi?',
        who: 'Etye Meyer',
        when: '7:45AM',
        notes: " I am mega gaylord ultima"
      }
    ];

    $scope.tasks = [
      {
        ExNum: '1',
        dueDate: '23/06/15',
        notes: " Build A Game: Scrabble"
      },
      {
        ExNum: '3',
        dueDate: '30/06/15',
        notes: " Static Array"
      },
      {
        ExNum: '4',
        dueDate: '07/07/15',
        notes: " Dynamic Array"
      },
    ];
  }
  else
  {
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
    $scope.prevText = '';
    document.getElementById("bindText").value = '';
    document.getElementById("msg").value = '';
    
  }

  $scope.clearAllClicked = function() // Clear Screen from text
  {
    document.getElementById("bindText").innerHTML = "";
  }

  // animation
  $scope.isEnterd = top.setIsEnterd;
}]);