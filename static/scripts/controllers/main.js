var app = angular.module('TestWise', ['ui.bootstrap', 'ui.router']);

app.controller('MainController', ['$uibModal', '$state', function($modal, $state){
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
      if(data) {
        // modalInstance.close('loggedin');
        $state.go('loggedin');
      }
    });
  };


  self.openRegisterDialog = function()
  {
    var modalInstance = $modal.open(
        {
          templateUrl: 'templates/registermodal.html',
          controller: 'LoginModalInstanceCtrl as ctrl',
          backdrop: 'static'
        }
    );
    modalInstance.result.then(function(data){
      // Set token on scope
      // self.token = data.token;
      if(data) {
        // modalInstance.close('loggedin');
        $state.go('loggedin');
      }
    });
  }



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
      },
      'loginbutton': {
        templateUrl: 'templates/loginbutton.html',
        controller: 'MainController',
        controllerAs: 'ctrl'
      }
    }
  });
  $stateProvider.state('loggedin', {
    url: '/',
    views: {
      '': {
        templateUrl: 'templates/home.html',
        controller: 'HomeController',
        controllerAs: 'ctrl'
      },
      'sidebar@loggedin': {
        templateUrl: 'templates/sidebar.html',
        controller: 'HomeController',
        controllerAs: 'ctrl'
      },
      'loginbutton': {
        templateUrl: 'templates/loggedinbanner.html',
        controller: 'HomeController',
        controllerAs: 'ctrl'
      }
    }
  });
  $stateProvider.state('loggedin.addtest', {
    url: '/',
    views: {
      'maincontent': {
        templateUrl: 'templates/addtest.html',
        controller: 'HomeController',
        controllerAs: 'ctrl'
      }
    }
  });
}]);
