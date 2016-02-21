angular.module('TestWise')
.controller('LoginModalInstanceCtrl', ['$uibModalInstance', '$http', function ($uibModalInstance, $http) {
  var self = this;
  self.cancel = function() {
    $uibModalInstance.close('cancel');
  };

  self.login = function() {
    // Login logic goes here
    $http.post('/login', {
        username: self.username,
        password: self.password
    })
    .success(function(data, status, headers, config){
      console.log(data);
      if(data["auth"] == 0) {
        // Not Logged in
        // Handle failed authentication
      } else {
        // Logged in
        $uibModalInstance.close(data);
      }
    });
  };

  self.cancelR = function() {
    $uibModalInstance.close('cancel');
  };

  self.register = function() {
    // Register logic goes here
    //console.log("Hello");
    $http.post('/register', {
        username: self.username,
        password: self.password,
        emailID: self.emailID
    })
    .success(function(data, status, headers, config){
      console.log(data);
      if(data["auth"] == 0) {
        // Not Logged in
        // Handle failed authentication
      } else {
        // Logged in
        $uibModalInstance.close(data);
      }
    });
  };



}]);
