var app = angular.module('TestWise', ['ui.bootstrap']);

app.controller('MainController', ['$uibModal', function($modal){
  var self = this;
  self.yourName = "Karthik";

  self.openLoginDialog = function() {
    var modalInstance = $modal.open({
      templateUrl: 'templates/loggedinmodal.html',
      controller: 'LoginModalInstanceCtrl as ctrl',
      backdrop: 'static'
    });
    modalInstance.result.then(function(data){
      // Set token on scope
      // self.token = data.token;
      // $state.go('loggedin');
    });
  };
}]);
