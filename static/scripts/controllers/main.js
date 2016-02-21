var app = angular.module('TestWise', ['ui.bootstrap', 'ui.router']);

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
}])
.config(['$urlRouterProvider', '$stateProvider', function($urlRouterProvider, $stateProvider){
  $urlRouterProvider.otherwise('/');
  $stateProvider.state('index', {
    url: '/',
    views: {
      '': {
        templateUrl: 'templates/landingpage.html',
        controller: 'MainController',
        controllerAs: 'ctrl'
      }
    }
  });
}]);
