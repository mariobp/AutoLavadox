angular.module('App', ['ngMaterial', 'ngMessages'])

.config(function($interpolateProvider, $mdThemingProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
	 $mdThemingProvider.theme('default')
    .primaryPalette('teal', {
			'default': '800'
		})
    .accentPalette('light-blue',{
			'default': 'A400'
		});
})

.controller('AppCtrl', function($scope, $http, $location, $mdDialog, $httpParamSerializer, $mdToast, $q) {
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
		$scope.serv1 = false;
		$scope.serv2 = false;
		$scope.serv3 = false;
		$scope.serv4 = false;
		$scope.serv5 = false;
		$scope.serv6 = false;
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
            location.href = "/empleados/login/";
        }, function failCallbacks(response){
            $scope.dialogError();
        });
    };

		//Lista de vehiculos
    $scope.listVehiculos = function(searchText){
				var deferred = $q.defer();
        $http({
          'url': '/cliente/vehiculo/?q='+ $scope.search,
          'method': 'GET'
        }).then(function doneCallbacks(response){
            //$scope.vehiculos = response.data.object_list;
						deferred.resolve(response.data.object_list);
        },function failCallbacks(response){
					  deferred.reject(response);
            $scope.dialogError();
        });
				return deferred.promise;
    };

		//Vehiculo seleccionado
    $scope.vehiculoActual = function($event){
			function placaRepetida(vehiculo) {
					return vehiculo.placa === $scope.selectedItem.placa;
			}
      if ($scope.selectedItem) {
					if ($scope.selectedItem.nombre && $scope.selectedItem.apellidos ) {
						$scope.nombre = $scope.selectedItem.nombre + " " + $scope.selectedItem.apellidos;
					}
          $scope.identificacion = $scope.selectedItem.cedula;
          $scope.tipo = $scope.selectedItem.tipov;
          if (!$scope.placas.includes($scope.selectedItem)) {
							var result = $scope.placas.find(placaRepetida);
						if (result === undefined) {
						   $scope.placas.push($scope.selectedItem);
						}else {
							if (result.ordenv) {
									$mdToast.show(
										$mdToast.simple()
											.textContent('Ya existe una orden para la placa '+ result.placa)
											.hideDelay(4000)
											.position('top start')
									);
							}
						}
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
						$scope.serv2 = true;
        },function failCallbacks(response){
            $scope.dialogError();
        });
    };


		//Lista de servicios aplicables
		$scope.serviciosList = function(){
				if (!$scope.selectedPlaca.ordenv) {
					$scope.serv5 = true;
					$scope.serv6 = true;
					console.log("entrooo a serv5");
					$scope.serviciosPorHacer = [];
					$http({
						'url': '/operacion/ws/tipo/servicio/?q='+ $scope.selectedPlaca.tipo,
						'method': 'GET',
					}).then(function doneCallbacks(response){
							$scope.servicios = response.data.object_list;
							$scope.serv5 = false;
							$scope.serv6 = false;
					}, function failCallbacks(response){
							$scope.serv5 = false;
							$scope.serv6 = false;
							$scope.dialogError();
					});
				}else {
					$scope.servicios = [];
					$scope.totalService = 0;
					$scope.serv5 = true;
					$scope.serv6 = true;
					$http({
						'url': '/operacion/ws/servicios/orden/?q='+ $scope.selectedPlaca.ordenv,
						'method': 'GET',
					}).then(function doneCallbacks(response){
							var data = response.data.object_list;
							$scope.serviciosPorHacer = data;
							data.forEach(function(item){
								$scope.servicios.push(item);
							});
							valor(data);
							habilitar();
							$scope.serv5 = false;
							$scope.serv6 = false;
					}, function failCallbacks(response){
							$scope.serv5 = false;
							$scope.serv6 = false;
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
								$scope.serv5 = false;
								$scope.serv6 = false;
					}, function failCallbacks(response){
							$scope.serv5 = false;
							$scope.serv6 = false;
							if (response.status == 500) {
								$scope.dialogError();
							}
					});
				}
		};

		function valor(array){
			$scope.totalService = 0;
			array.forEach(function(item){

				if (item.status) {
					$scope.totalService+= item.valor;
				}
			});
		}

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
						servicio.id = response.data.id;
						servicio.tipo = response.data.tipo_id;
						servicio.status = !servicio.status;
						$scope.serviciosPorHacer.push(servicio);
						valor($scope.serviciosPorHacer);
						$scope.serv5 = false;
						$scope.serv6 = false;
						$mdToast.show(
							$mdToast.simple()
								.textContent('Guardado Exitoso')
								.hideDelay(3000)
								.position('bottom start')
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
					$scope.serv5 = true;
					$scope.serv6 = true;
					$http({
						'url':'/operacion/cancel/servicio/'+servicio.id+'/',
						'method': 'GET'
					}).then(function doneCallbacks(response){
							$scope.serv5 = false;
							$scope.serv6 = false;
							servicio.status = !servicio.status;
							removeFromArray($scope.serviciosPorHacer, servicio);
							valor($scope.serviciosPorHacer);
							$mdToast.show(
								$mdToast.simple()
									.textContent('Servicio cancelado')
					        .hideDelay(3000)
									.position('bottom start')
							);
					}, function failCallbacks(response){
							$scope.serv5 = false;
							$scope.serv6 = false;
							if (response.status == 500) {
								$scope.dialogError();
							}
						});
				}, function() {

				});
			}else {
					$scope.serv5 = true;
					$scope.serv6 = true;
					if ($scope.selectedPlaca.ordenv) {
							data.orden = $scope.selectedPlaca.ordenv;
							if (servicio.tipo) {
									data.tipo = servicio.tipo;
							} else {
									data.tipo = servicio.id;
							}
							data.operario = servicio.operario;
							registrarServicio(data, servicio);
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
									$scope.selectedPlaca.tipo = $scope.selectedPlaca.tipo;
									data.orden = response.data.id;
									data.tipo = servicio.id;
									data.operario = servicio.operario;
									registrarServicio(data, servicio);
										$mdToast.show(
											$mdToast.simple()
												.textContent('Servicio asignado')
								        .hideDelay(3000)
												.position('bottom start')
										);
							}, function failCallbacks(response){
									$scope.serv5 = false;
									$scope.serv6 = false;
									if (response.status == 500) {
											$scope.dialogError();
									}
							});
					}
			}
		};

		//Servicio para asignar un operario a un servicio
		$scope.asignarOperarioDialog = function(servicio, ev){
				  var dialog = $mdDialog.show({
			      template:
			      '<md-dialog aria-label="operarios">' +
			        '<form ng-cloak name="form">' +
			          '<md-toolbar>' +
			            '<div class="md-toolbar-tools">' +
			              '<h2>Operarios</h2>' +
			              '<span flex></span>' +
			            '</div>' +
			          '</md-toolbar>' +
			          '<md-dialog-content>' +
			            '<div class="md-dialog-content">' +
			              '<md-list >' +
			                 '<md-list-item ng-click="null" ng-repeat="operario in operarios">' +
			                    '<p>[[operario.nombre]]</p>' +
			                    '<md-checkbox class="md-secondary" ng-model="operario.elegido"></md-checkbox>' +
			                '</md-list-item>' +
			              '</md-list >' +
			            '</div>'+
			          '</md-dialog-content>'+
			          '<md-dialog-actions layout="row">'+
			            '<md-button class="md-raised red" ng-click="closeDialog()" flex>'+
			              'Cancelar'+
			            '</md-button>'+
			            '<md-button class="md-primary md-raised" ng-click="asignarOperario()" flex>'+
			              'Agregar'+
			            '</md-button>'+
			          '</md-dialog-actions>'+
			        '</form>'+
			      '</md-dialog>',
			      controller: 'Dialog2Controller',
			      locals: {
			        data: $scope.operarios,
			        servicio: servicio,
							orden: $scope.selectedPlaca.ordenv,
							tipo: $scope.selectedPlaca.tipo,
							dialogError: $scope.dialogError,
			      },
			      clickOutsideToClose:true,
			      parent: angular.element(document.querySelector('#popupContainer')),
						targetEvent: ev,
			    }).then(function(){

			    },function(){

			    });
		};

		//Lista de operarios
		$scope.operariosList = function () {
				$http({
					'url':'/empleados/operarios/',
					'method': 'GET'
				}).then(function doneCallbacks(response){
						$scope.operarios = response.data.object_list;
						$scope.serv3 = true;
				}, function failCallbacks(response){
						if (response.status == 500) {
								$scope.dialogError();
						}
				});
		};

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
						$scope.serv4 = true;
				}, function failCallbacks(response){
						if (response.status == 500) {
								$scope.dialogError();
						}
				});
		};

		//Invocar servicios
		$scope.tipoVehiculo();
		$scope.operariosList();
		$scope.ordenesPendientes();

		function habilitar(){
				var n = $scope.serviciosPorHacer.length;
				if (n > 0) {
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
								.position('bottom start')
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
								valor($scope.serviciosPorHacer);
								$mdToast.show(
									$mdToast.simple()
										.textContent('Orden finalizada')
						        .hideDelay(3000)
										.position('bottom start')
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
						placa: $scope.search,
						placas: $scope.placas,
						tipo: $scope.tipo,
						nombre: $scope.nombre,
						identificacion: $scope.identificacion,
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
.controller('Dialog2Controller', function($scope, $mdDialog, $http, $mdToast, $httpParamSerializer, data, servicio, orden, tipo, dialogError){
		$scope.closeDialog = function() {
			  $mdDialog.hide();
		};

		$scope.operarios = data;
		var dataSend = {};
		dataSend.operario = [];

		function selectCheck(){
			$scope.operarios.forEach(function(item){
				if (item.elegido) {
					dataSend.operario.push(item.id);
				}
			});
		}

		$scope.asignarOperario = function(){
				if(orden){
					$mdDialog.hide();
					$mdToast.show(
						$mdToast.simple()
							.textContent('Guardando...')
							.hideDelay(3000)
							.position('bottom start')
					);
					selectCheck();
					dataSend.orden = orden;
					dataSend.tipo = tipo;
					$http({
						'url': '/operacion/edit/servicio/'+ servicio.id +'/',
						 'method': 'POST',
						 'data': dataSend,
			 			  headers: {
			 						'Content-Type': 'application/x-www-form-urlencoded'
			 				},
					}).then(function doneCallbacks(response){
							$mdDialog.hide();
							$mdToast.show(
								$mdToast.simple()
									.textContent('Guardado Exitoso')
					        .hideDelay(3000)
									.position('bottom start')
							);
					}, function failCallbacks(response){
							if (response.status == 500) {
									dialogError();
							}
					});
				}
		};
})
.controller('DialogController', function($scope, $http, $mdDialog, $mdToast, $httpParamSerializer, placa, placas, tipos, tipo, nombre, identificacion){
		$scope.tipos = tipos;
		$scope.data = {};
		$scope.data.placa = placa;
		$scope.closeDialog = function() {
			  $mdDialog.hide();
		};

		$scope.enviar = function(){
			$http({
				url:'/cliente/add/vehiculo/',
				method: 'POST',
				data: $httpParamSerializer($scope.data),
			  headers: {
						'Content-Type': 'application/x-www-form-urlencoded'
				},
			}).then(function doneCallbacks(response){
					var item = {};
					item.placa = response.data.placa;
					item.tipo = response.data.tipo_id;
					item.id = response.data.id;
					placas.push(item);

					function searchTipo(tipo){
						return tipo.id == response.data.tipo_id;
					}
					var result = tipos.find(searchTipo);
					tipo = result.nombre;
					identificacion = "Sin registrar";
					nombre = "Sin registrar";
					$mdDialog.hide();
					$mdToast.show(
						$mdToast.simple()
							.textContent('Guardado Exitoso')
			        .hideDelay(3000)
						  .position('bottom start')
					);
			}, function failCallbacks(response){
					console.log(response);
					if (response.status == 400) {
						if (response.data.placa) {
							$mdToast.show(
								$mdToast.simple()
									.textContent("Placa: " + response.data.placa[0])
									.position('bottom start')
					        .hideDelay(3000)
							);
						}else if(response.data.tipo){
							$mdToast.show(
								$mdToast.simple()
									.textContent("Tipo: " + response.data.tipo[0])
									.position('bottom start')
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
