wusApp = angular.module('wusApp',[
    'ngRoute',
    'wusControllers'
    ])

wusApp.config(['$routeProvider', 
    function($routeProvider){
      $routeProvider.
        when('/', {
          templateUrl: '/static/partials/index.html'
        }).
        when('/login',{
          templateUrl: '/static/partials/login.html'
        }).
        when('/admin', {
          templateUrl: '/static/partials/admin.html'
        }).
        when('/wus', {
          templateUrl: '/static/partials/wus.html'
        }).
        otherwise('/', {
          templateUrl: '/static/partials/index.html'
        })
    }])
