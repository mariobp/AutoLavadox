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
		$scope.serviciosPorHacer = [];
    $scope.tipos = [];
		$scope.selectedPlaca = {};
		$scope.operarios = [];
		$scope.totalService= 0;
		$scope.habilitarOrden = true;
		var data = {};
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
					$scope.servicios = [];
					$scope.totalService = 0;
					$http({
						'url': '/operacion/ws/servicios/orden/?q='+ $scope.selectedPlaca.ordenv,
						'method': 'GET',
					}).then(function doneCallbacks(response){
							var data = response.data.object_list;
							$scope.serviciosPorHacer = data;
							data.forEach(function(item){
								$scope.servicios.push(item);
								$scope.totalService+= item.valor;
							});
							habilitar();
					}, function failCallbacks(response){
							$scope.dialogError();
					});
					$http({
						'url': '/operacion/ws/tipo/servicio/por/asignar/?tipo='+$scope.selectedPlaca.tipo+"&orden="+$scope.selectedPlaca.ordenv,
						'method': 'GET'
					}).then(function doneCallbacks(response){
								var data = response.data.object_list;
								data.forEach(function(item){
									$scope.servicios.push(item);
								});
					}, function failCallbacks(response){
							if (response.status == 500) {
								$scope.dialogError();
							}
					});
				}
		};

		//Agrega servicio
		function registrarServicio(data, servicio){
				$http({
					'url': '/operacion/add/servicio/',
					'method': 'POST',
					'data': $httpParamSerializer(data),
					 headers: {
							 'Content-Type': 'application/x-www-form-urlencoded'
					 }
				}).then(function doneCallbacks(response){
						console.log(response);
						servicio.id = response.data.id;
						servicio.tipoid = response.data.tipo;
						$mdToast.show(
							$mdToast.simple()
								.textContent('Guardado Exitoso')
								.hideDelay(3000)
						);
				}, function failCallbacks(response){
						if (response.status == 500) {
								$scope.dialogError();
						}
				});
		}


		$scope.changeCheck = function (servicio) {
			if(servicio.status){
			  var confirm = $mdDialog.confirm()
	      .title('Estas seguro que quieres cancelar?')
	      .ariaLabel('Lucky day')
	      .ok('Si')
	      .cancel('No');
				$mdDialog.show(confirm).then(function() {
					$http({
						'url':'/operacion/cancel/servicio/'+servicio.id+'/',
						'method': 'GET'
					}).then(function doneCallbacks(response){
							servicio.status = !servicio.status;
							$mdToast.show(
								$mdToast.simple()
									.textContent('Servicio cancelado')
					        .hideDelay(3000)
							);
					}, function failCallbacks(response){
							if (response.status == 500) {
								$scope.dialogError();
							}
						});
				}, function() {

				});
			}else {
					if ($scope.selectedPlaca.ordenv) {
							data.orden = $scope.selectedPlaca.ordenv;
							data.tipo = servicio.id;
							data.operario = servicio.operario;
							registrarServicio(data);
					}else {
							data.vehiculo = $scope.selectedPlaca.id;
							$http({
								'url': '/operacion/add/orden/',
								'method': 'POST',
								'data': $httpParamSerializer(data),
								 headers: {
										 'Content-Type': 'application/x-www-form-urlencoded'
								 },
							}).then(function doneCallbacks(response){
									$scope.selectedPlaca.ordenv = response.data.id;
									data.orden = response.data.id;
									data.tipo = servicio.id;
									data.operario = servicio.operario;
									registrarServicio(data, servicio);
									servicio.status = !servicio.status;
										$mdToast.show(
											$mdToast.simple()
												.textContent('Servicio asignado')
								        .hideDelay(3000)
										);
							}, function failCallbacks(response){
									if (response.status == 500) {
											$scope.dialogError();
									}
							});
					}
			}
		};

		//Servicio para asignar un operario a un servicio
		$scope.asignarOperario = function(operario, servicio){
				if($scope.selectedPlaca.ordenv){
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
									$scope.dialogError();
							}
					});
				}else {
						servicio.operario =  operario.id;
						servicio.operario_nombre = operario.nombre;
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
						if (response.status == 500) {
								$scope.dialogError();
						}
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
						if (response.status == 500) {
								$scope.dialogError();
						}
				});
		};
		$scope.ordenesPendientes();

		function habilitar(){
				var n = $scope.serviciosPorHacer.length;
				if (n>0) {
					$scope.serviciosPorHacer.forEach(function(item){
							if(item.estado){
								n = n - 1;
							}
					});
					if(n===0){
						$scope.habilitarOrden = false;
					}else {
						$scope.habilitarOrden = true;
					}
				}else {
					$scope.habilitarOrden = true;
				}

		}

		function removeFromArray(array, element){
			var index = array.indexOf(element);
			if (index > -1) {
			  array.splice(index, 1);
			}
		}

		$scope.servicioListo = function(service){
			function findService(item){
					return item === service;
			}

			function enviar(){
				$http({
					'url': '/operacion/ok/servicio/'+ service.id+'/',
					'method': 'GET'
				}).then(function doneCallbacks(response){
						console.log(response);
						var num = $scope.servicios.find(findService);
						console.log(num);
						console.log(service);
						service.estado = !service.estado;
						num.estado = service.estado;
						habilitar();
						$mdToast.show(
							$mdToast.simple()
								.textContent('Guardado Exitoso')
				        .hideDelay(3000)
						);
				},function failCallbacks(response){
						if (response.status == 500) {
								$scope.dialogError();
						}
				});
			}
			enviar();
		};

		$scope.cerrarOrden = function(){
			  var confirm = $mdDialog.confirm()
	      .title('Estas seguro que quieres cerrar la Orden?')
				.textContent('No se podra modificar una vez se cierre.')
	      .ariaLabel('DD')
	      .ok('Si')
	      .cancel('Cancelar');
				$mdDialog.show(confirm).then(function() {
						$http({
							'url': '/operacion/close/orden/'+$scope.selectedPlaca.ordenv,
							'method': 'GET'
						}).then(function doneCallbacks(response){
								$scope.servicios = [];
								$scope.serviciosPorHacer = [];
								removeFromArray($scope.placas, $scope.selectedPlaca);
								$mdToast.show(
									$mdToast.simple()
										.textContent('Orden finalizada')
						        .hideDelay(3000)
								);
						},function failCallbacks(response){
								if (response.status == 500) {
										$scope.dialogError();
								}
						});
				}, function() {

				});

		};

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
