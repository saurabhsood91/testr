angular.module('TestWise')
.controller('LoginModalInstanceCtrl', ['$uibModal', '$http', function ($uibModal, $http) {
  var self = this;
}]);
  // self.login = function() {
  //   // Login logic goes here
  //   $http.post('/login', {
  //     params: {
  //       username: self.username,
  //       password: self.password
  //     }
  //   })
  //   .success(function(data, status, headers, config){
  //     console.log(data);
  //     if(data["auth"] == 0) {
  //       // Not Logged in
  //       // Handle failed authentication
  //     } else {
  //       // Logged in
  //       $modalInstance.close(data);
  //     }
  //   });
  // };
