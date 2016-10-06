angular.module('App', ['ngMaterial', 'ngMessages'])

.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
})

.controller('AppCtrl', function($scope, $http, $location, $mdDialog) {

    $scope.cerrarSesion = function(){
        $http({
          'url': '/empleados/logout/',
          'method': 'GET',
        }).then(function doneCallbacks(response){
            location.href = "/login/";
        }, function failCallbacks(response){
            $mdDialog.show(
              $mdDialog.alert()
                .parent(angular.element(document.querySelector('#popupContainer')))
                .clickOutsideToClose(true)
                .title('Error del servidor')
                .textContent('Hay un error, contacte a el administrador.')
                .ariaLabel('Alert Dialog Error')
                .ok('OK')
            );
        });
    };

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
