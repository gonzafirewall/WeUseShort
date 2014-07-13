wusControllers = angular.module('wusControllers', [])

wusControllers.factory('Auth', function($http){
  return {
    logout: function (){
      return $http.get('/logout');
    },
    login: function(inputs){
      return $http.post('/api/login', inputs);
    }
  }
});

wusControllers.controller('mainCtrl', ['$scope', '$location','Auth', function($scope, $location, Auth){
  $scope.user = {}  
  $scope.cred = {};
  $scope.loadUser = function (){
    
  };
  $scope.login = function(cred){
    Auth.login(cred)
      .success(function(data){
        if (data.result == 'success') {
          $scope.user = {id: 1};
          $location.path('/admin');
        }
      })
  };
  $scope.logout = function(){
    Auth.logout()
      .success(function(data){
        $scope.user = {};
        $location.path('/');
      })
  };

}]);

wusControllers.controller('loginCtrl' ['$scope', function($scope){
  
}])

wusControllers.controller('shorterCtrl', ['$scope', '$http', '$location', function($scope, $http, $location){
  $scope.shortUrl = ""
  $scope.shorters = []
  $scope.loadUrls = function (){
    $http.get('/api/url')
      .success( function(data){
        console.log(data);
        $scope.shorters = data
      });
  };
  $scope.loadUrls();
  $scope.short = function (url){
    $http.post('/admin/', {'url': url})
      .success(function(data){
        if (data.result == 'success') {
          $scope.shortUrl = data.shortUrl;
          $scope.loadUrls();
        };
        if (data.result == 'fail') {
          if (data.info == 'login_need')  {
            $location.path('/login')
          };
        }
      });
  };
}])
