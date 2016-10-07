angular.module('App', ['ngMaterial', 'ngMessages'])

.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
})

.controller('AppCtrl', function($scope, $http, $location, $mdDialog) {
    $scope.search = "";
    $scope.vehiculos = [];
    $scope.nombre = "";
    $scope.identificacion = "";
    $scope.placas = [];
    $scope.tipo = "";
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
    $scope.tipos = [];
    $scope.dialog = function(){
      $mdDialog.show(
        $mdDialog.alert()
          .parent(angular.element(document.querySelector('#popupContainer')))
          .clickOutsideToClose(true)
          .title('Error del servidor')
          .textContent('Hay un error, contacte a el administrador.')
          .ariaLabel('Alert Dialog Error')
          .ok('OK')
      );
    };

    $scope.cerrarSesion = function(){
        $http({
          'url': '/empleados/logout/',
          'method': 'GET',
        }).then(function doneCallbacks(response){
            location.href = "/login/";
        }, function failCallbacks(response){
            $scope.dialog();
        });
    };

    $scope.listVehiculos = function(searchText){
        $http({
          'url': '/cliente/vehiculo/?q='+ $scope.search,
          'method': 'GET'
        }).then(function doneCallbacks(response){
            $scope.vehiculos = response.data.object_list;
        },function failCallbacks(response){
            $scope.dialog();
        });
    };
    $scope.listVehiculos();

    $scope.vehiculoActual = function(){
      console.log($scope.selectedItem);
      if ($scope.selectedItem) {
          $scope.nombre = $scope.selectedItem.nombre + " " + $scope.selectedItem.apellidos;
          $scope.identificacion = $scope.selectedItem.cedula;
          $scope.tipo = $scope.selectedItem.tipov;
          if (!$scope.placas.includes($scope.selectedItem)) {
              $scope.placas.push($scope.selectedItem);
          }
      }else {
          $scope.nombre = "";
          $scope.identificacion = "";
          $scope.tipo = "";
      }
    };

    $scope.tipoVehiculo = function(){
        $http({
          'url': '/cliente/tipo/vehiculo/',
          'method': 'GET'
        }).then(function doneCallbacks(response){
            $scope.tipos = response.data.object_list;
        },function failCallbacks(response){
            $scope.dialog();
        });
    };
    $scope.tipoVehiculo();

    $scope.nuevo = function(placa) {
          alert("Registrando");
    };

});
