angular.module('App', ['ngMaterial', 'ngMessages'])

.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
})

.controller('AppCtrl', function($scope, $http, $location, $mdDialog, $httpParamSerializer, $mdToast) {
    $scope.search = "";
    $scope.vehiculos = [];
    $scope.nombre = "";
    $scope.identificacion = "";
    $scope.placas = [];
    $scope.tipo = "";
    $scope.servicios = [];
    $scope.tipos = [];
		$scope.selectedPlaca = {};
		$scope.operarios = [];
    $scope.dialogError = function(){
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

		//Servicio para cerrar sesión
    $scope.cerrarSesion = function(){
        $http({
          'url': '/empleados/logout/',
          'method': 'GET',
        }).then(function doneCallbacks(response){
            location.href = "/login/";
        }, function failCallbacks(response){
            $scope.dialogError();
        });
    };

		//Lista de vehiculos
    $scope.listVehiculos = function(searchText){
        $http({
          'url': '/cliente/vehiculo/?q='+ $scope.search,
          'method': 'GET'
        }).then(function doneCallbacks(response){
            $scope.vehiculos = response.data.object_list;
        },function failCallbacks(response){
            $scope.dialogError();
        });
    };
    $scope.listVehiculos();

		//Vehiculo seleccionado
    $scope.vehiculoActual = function(){
      console.log($scope.selectedItem);
      if ($scope.selectedItem) {
					if ($scope.selectedItem.nombre && $scope.selectedItem.apellidos ) {
						$scope.nombre = $scope.selectedItem.nombre + " " + $scope.selectedItem.apellidos;
					}
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

		//Servicio de los tipos de vehiculos
    $scope.tipoVehiculo = function(){
        $http({
          'url': '/cliente/tipo/vehiculo/',
          'method': 'GET'
        }).then(function doneCallbacks(response){
            $scope.tipos = response.data.object_list;
        },function failCallbacks(response){
            $scope.dialogError();
        });
    };
    $scope.tipoVehiculo();

		//Lista de servicios aplicables
		$scope.serviciosList = function(){
				if ($scope.selectedPlaca.tipoid) {
					$http({
						'url': '/operacion/ws/tipo/servicio/?q='+ $scope.selectedPlaca.tipoid,
						'method': 'GET',
					}).then(function doneCallbacks(response){
							$scope.servicios = response.data.object_list;
					}, function failCallbacks(response){
							$scope.dialogError();
					});
				}else if ($scope.selectedPlaca.ordenv) {
					$http({
						'url': '/operacion/ws/servicios/orden/?q='+ $scope.selectedPlaca.ordenv,
						'method': 'GET',
					}).then(function doneCallbacks(response){
							$scope.servicios = response.data.object_list;
					}, function failCallbacks(response){
							$scope.dialogError();
					});
				}

		};

		$scope.changeCheck = function (servicio) {
			if(servicio.checked){
				servicio.checked = !servicio.checked;
				console.log($scope.selectedPlaca);
				console.log(servicio);
			}
		};

		$scope.asignarOperario = function(operario, servicio){
				console.log(servicio);
				console.log($scope.selectedPlaca);
				if($scope.selectedPlaca.ordenv){
					var data = {};
					data.orden = $scope.selectedPlaca.ordenv;
					data.tipo = servicio.tipoid;
					data.operario = operario.id;
					$http({
						'url': '/operacion/edit/servicio/'+ servicio.id +'/',
						 'method': 'POST',
						 'data': $httpParamSerializer(data),
			 			  headers: {
			 						'Content-Type': 'application/x-www-form-urlencoded'
			 				},
					}).then(function doneCallbacks(response){
							servicio.operario =  operario.id;
							servicio.operario_nombre = operario.nombre;
							$mdDialog.hide();
							$mdToast.show(
								$mdToast.simple()
									.textContent('Guardado Exitoso')
					        .hideDelay(3000)
							);
					}, function failCallbacks(response){
							if (response.status == 500) {
								$mdDialog.show(
									$mdDialog.alert()
										.parent(angular.element(document.querySelector('#popupContainer')))
										.clickOutsideToClose(true)
										.title('Error del servidor')
										.textContent('Hay un error, contacte a el administrador.')
										.ariaLabel('Alert Dialog Error')
										.ok('OK')
								);
							}
					});
				}
		};

		//Lista de operarios
		$scope.operariosList = function () {
				$http({
					'url':'/empleados/operarios/',
					'method': 'GET'
				}).then(function doneCallbacks(response){
						$scope.operarios = response.data.object_list;
				}, function failCallbacks(response){
						$scope.dialogError();
				});
		};
		$scope.operariosList();

		//Ordenes sin terminar
		$scope.ordenesPendientes = function(){
				$http({
					'url': '/operacion/get/ordenes/pendientes/',
					'method': 'GET'
				}).then(function doneCallbacks(response){
						var data = response.data.object_list;
						data.forEach(function(item){
							$scope.placas.push(item);
						});
				}, function failCallbacks(response){
						$scope.dialogError();
				});
		};
		$scope.ordenesPendientes();

		//Agrega nuevo vechiculo
    $scope.nuevo = function(placa) {
        $mdDialog.show({
          templateUrl: '/template/add/',
					controller: 'DialogController',
          clickOutsideToClose:true,
					locals: {
						tipos:$scope.tipos,
						placa: $scope.search
					}

           // Only for -xs, -sm breakpoints.
        })
        .then(function(answer) {
					console.log("entro");
          $scope.status = 'You said the information was "' + answer + '".';
        }, function(a) {
					console.log(a);
					console.log("entro");
          $scope.status = 'You cancelled the dialog.';
        });
    };
})

.controller('DialogController', function($scope, $http, $mdDialog, $mdToast, $httpParamSerializer, placa, tipos){
		$scope.tipos = tipos;
		$scope.data = {};
		$scope.data.placa = placa;
		var formData = new FormData();

		$scope.closeDialog = function() {
			  $mdDialog.hide();
		};

		$scope.enviar = function(){
			formData.append('placa', $scope.data.placa);
			formData.append('tipo', $scope.data.tipo);
			$http({
				url:'/cliente/add/vehiculo/',
				method: 'POST',
				data: $httpParamSerializer($scope.data),
			  headers: {
						'Content-Type': 'application/x-www-form-urlencoded'
				},
			}).then(function doneCallbacks(response){
					console.log(response);
					$mdDialog.hide();
					$mdToast.show(
						$mdToast.simple()
							.textContent('Guardado Exitoso')
			        .hideDelay(3000)
					);
			}, function failCallbacks(response){
					console.log(response);
					if (response.status == 400) {
						console.log("400");
						console.log(response.data.placa);
						if (response.data.placa) {
							$mdToast.show(
								$mdToast.simple()
									.textContent("Placa: " + response.data.placa[0])
									.position("bottom")
					        .hideDelay(3000)
							);
						}else if(response.data.tipo){
							$mdToast.show(
								$mdToast.simple()
									.textContent("Tipo: " + response.data.tipo[0])
									.position("bottom")
					        .hideDelay(3000)
							);
						}
					}else if (response.status == 500) {
						$mdDialog.show(
							$mdDialog.alert()
								.parent(angular.element(document.querySelector('#popupContainer')))
								.clickOutsideToClose(true)
								.title('Error del servidor')
								.textContent('Hay un error, contacte a el administrador.')
								.ariaLabel('Alert Dialog Error')
								.ok('OK')
						);
					}
			});
		};
});
