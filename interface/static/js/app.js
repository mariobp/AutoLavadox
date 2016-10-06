angular.module('App', ['ngMaterial', 'ngMessages'])

.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
})

.controller('AppCtrl', function($scope, $http) {
    $scope.hola = "Hola Mundo";
    $scope.placas = [{
        id: 1,
        numero: "720WW"
    }, {
        id: 2,
        numero: "541MF"
    }, {
        id: 3,
        numero: "666XX"
    }, ];

    $scope.selectedId = 2;

    $scope.servicios = [
      {
        nombre: "Lavado",
        id:1
      },
      {
        nombre: "Pulida",
        id:2
      },
      {
        nombre: "Cambio de aceite",
        id:3
      },
      {
        nombre: "Lavado",
        id:4
      },
      {
        nombre: "Pulida",
        id:5
      },
      {
        nombre: "Cambio de aceite",
        id:6
      }
    ];

    $scope.tipos = [
      {
        id:1,
        nombre: "Camión"
      },
      {
        id:2,
        nombre: "Deportivo"
      }
    ];
});
