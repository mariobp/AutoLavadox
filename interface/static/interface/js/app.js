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

.controller('AppCtrl', function($scope, $http, $location, $mdDialog, $httpParamSerializer, $mdToast, $q, $window) {
	  $window.onbeforeunload = function(){
	    return confirm("Are you sure you want to navigate away from this page");
	  };
    $scope.search = "";
    $scope.vehiculos = [];
    $scope.placas = [];
		$scope.info = {};
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
		$scope.serv7 = false;
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
						$scope.info.nombre = $scope.selectedItem.nombre + " " + $scope.selectedItem.apellidos;
					}
					if ($scope.selectedItem.color) {
						$scope.info.color = $scope.selectedItem.color;
					}if ($scope.selectedItem.marca) {
						$scope.info.marca = $scope.selectedItem.marca;
					}if ($scope.selectedItem.kilometraje) {
						$scope.info.kilometraje = $scope.selectedItem.kilometraje;
					}
					$scope.info.celular = $scope.selectedItem.celular;
          $scope.info.identificacion = $scope.selectedItem.cedula;
          $scope.info.tipo = $scope.selectedItem.tipov;
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
          $scope.info.nombre = "";
          $scope.info.identificacion = "";
          $scope.info.tipo = "";
					$scope.info.celular = "";
					$scope.info.marca = "";
					$scope.info.color = "";
					$scope.info.kilometraje = "";
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
							$scope.servicios = [];
							data.forEach(function(item){
								$scope.servicios.push(item);
							});
							valor(data);
							habilitar();
							$scope.serv5 = false;
							porasignar();
					}, function failCallbacks(response){
							$scope.serv5 = false;
							$scope.dialogError();
					});

					function porasignar() {
						$http({
							'url': '/operacion/ws/tipo/servicio/por/asignar/?tipo='+$scope.selectedPlaca.tipo+"&orden="+$scope.selectedPlaca.ordenv,
							'method': 'GET'
						}).then(function doneCallbacks(response){
									var data = response.data.object_list;
									data.forEach(function(item){
										$scope.servicios.push(item);
									});
									$scope.serv6 = false;
						}, function failCallbacks(response){
								$scope.serv6 = false;
								if (response.status == 500) {
									$scope.dialogError();
								}
						});
					}
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
					'data': data,
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
								.position('top right')
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
									.position('top right')
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
												.position('top right')
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
									'<div layout="row" layout-align="center center" ng-if="cargando" style="height:200px">' +
											'<md-progress-circular ng-disabled="!cargando" md-mode="indeterminate" md-diameter="50"></md-progress-circular>' +
									'</div>' +
			            '<div class="md-dialog-content"  ng-if="!cargando">' +
			              '<md-list >' +
			                 '<md-list-item ng-click="null" ng-repeat="operario in operarios">' +
			                    '<p>[[operario.nombre]]</p>' +
			                    '<md-checkbox class="md-secondary" ng-model="operario.elegido"></md-checkbox>' +
			                '</md-list-item>' +
			              '</md-list >' +
			            '</div>'+
			          '</md-dialog-content>'+
			          '<md-dialog-actions  ng-if="!cargando" layout="row">'+
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
			$scope.serv7 = true;
			function enviar(){
				$http({
					'url': '/operacion/ok/servicio/'+ service.id+'/',
					'method': 'GET'
				}).then(function doneCallbacks(response){
						var num = $scope.servicios.find(findService);
						service.estado = !service.estado;
						num.estado = service.estado;
						habilitar();
						$mdToast.show(
							$mdToast.simple()
								.textContent('Guardado Exitoso')
				        .hideDelay(3000)
								.position('top right')
						);
						$scope.serv7 = false;
				},function failCallbacks(response){
						$scope.serv7 = false;
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
						$scope.serv6 = true;
						$scope.serv7 = true;
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
										.position('top right')
								);
								$scope.serv6 = false;
								$scope.serv7 = false;
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
          template:
						'<md-dialog aria-label="Registrar Vehículo">' +
						  '<form ng-cloak name="form" ng-submit="form.$valid && enviar()" novalidate>' +
						    '<md-toolbar>' +
						      '<div class="md-toolbar-tools">' +
						        '<h2>Registrar Vehículo</h2>' +
						        '<span flex></span>' +
						        '<md-button class="md-icon-button" ng-click="closeDialog()">' +
						          '<md-icon md-svg-src="media/iconos/ic_close_white.svg" aria-label="Close dialog"></md-icon>' +
						        '</md-button>' +
						      '</div>' +
						    '</md-toolbar>' +
						    '<md-dialog-content>' +
						  		'<div layout="row" layout-align="center center" ng-if="cargando" style="height:200px">' +
						  				'<md-progress-circular ng-disabled="!cargando" md-mode="indeterminate" md-diameter="50"></md-progress-circular>' +
						  		'</div>' +
						      '<div class="md-dialog-content" ng-if="!cargando">' +
									'<div layout="row">' +
		                '<md-autocomplete md-input-name="identificacion" md-floating-label="Identificación" md-no-float md-selected-item="selectedCliente" md-no-cache="true" md-min-length="0" md-selected-item-change="clienteActual($event)"	md-search-text-change="textChange2(search2)" md-search-text="search2" md-items="cliente in listClientes(search2)" md-item-text="cliente.identificacion" placeholder="Escribir el numero de identificación" flex>' +
											'<span md-highlight-text="search">[[cliente.nombre]] [[cliente.apellidos]] - [[cliente.identificacion]]</span>' +
											 '<md-not-found>' +
												'No hay hay resultados para "[[search2]]"' +
											'</md-not-found>' +
											'<div ng-messages="form.identificacion.$error" ng-if="form.autocompleteField.$touched">' +
												'<div ng-message="required">Este campo es requerido.</div>' +
											'</div>' +
										'</md-autocomplete >' +
		              '</div>' +
									'<div layout="row">' +
		                '<md-autocomplete md-input-name="celular" md-floating-label="Celular" md-no-float md-selected-item="selectedCliente" md-no-cache="true" md-min-length="0" md-selected-item-change="clienteActual($event)"	md-search-text-change="textChange3(search3)" md-search-text="search3" md-items="cliente in listClientes(search3)" md-item-text="cliente.celular" placeholder="Escribir el numero de celular" flex required>' +
											'<span md-highlight-text="search">[[cliente.nombre]] [[cliente.apellidos]] - [[cliente.celular]]</span>' +
											 '<md-not-found>' +
												'No hay hay resultados para "[[search3]]"' +
											'</md-not-found>' +
											'<div ng-messages="form.celular.$error" ng-if="form.autocompleteField.$touched">' +
												'<div ng-message="required">Este campo es requerido.</div>' +
											'</div>' +
										'</md-autocomplete >' +
		              '</div>' +
		              '<div layout="row" layout-xs="column" >' +
		                '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100" >' +
		                   '<label>Nombre</label>' +
		                    '<input type="text" ng-model="data.nombre" name="nombre" value="" required>' +
		                    '<div ng-messages="form.nombre.$error">' +
		                      '<div ng-message="required">Este campo es requerido.</div>' +
		                    '</div>' +
		                '</md-input-container>' +
		                '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100" >' +
		                   '<label>Apellidos</label>' +
		                    '<input type="text" ng-model="data.apellidos" name="apellidos" value="" required>' +
		                    '<div ng-messages="form.apellidos.$error">' +
		                      '<div ng-message="required">Este campo es requerido.</div>' +
		                    '</div>' +
		                '</md-input-container>' +
		              '</div>' +
										'<div layout="row" layout-xs="column">' +
			                  '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
			                    '<label>Placa</label>' +
			                    '<input ng-model="data.placa" name="placa" required>' +
			                    '<div ng-messages="form.placa.$error">' +
			                      '<div ng-message="required">Este campo es requerido.</div>' +
			                    '</div>' +
			                  '</md-input-container>' +
									      '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
								          '<label>Marca</label>' +
								          '<input ng-model="data.marca" name="marca" required>' +
								          '<div ng-messages="form.marca.$error">' +
								            '<div ng-message="required">Este campo es requerido.</div>' +
								          '</div>' +
								        '</md-input-container>' +
			              '</div>' +
										'<div layout="row" layout-xs="column">' +
											'<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
												'<label>Color</label>' +
												'<input ng-model="data.color" name="color" required>' +
												'<div ng-messages="form.color.$error">' +
													'<div ng-message="required">Este campo es requerido.</div>' +
												'</div>' +
											'</md-input-container>' +
											'<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
												'<label>Kilometraje</label>' +
												'<input ng-model="data.kilometraje" name="kilometraje" required>' +
												'<div ng-messages="form.kilometraje.$error">' +
													'<div ng-message="required">Este campo es requerido.</div>' +
												'</div>' +
											'</md-input-container>' +
										'</div>' +
						        '<md-input-container class="md-block" >' +
						           '<label>Tipo</label>' +
						            '<md-select ng-model="data.tipo" name="tipo" required>' +
						              '<md-option ng-repeat="tipo in tipos"  value="[[tipo.id]]">' +
						                '[[tipo.nombre]]' +
						              '</md-option>' +
						            '</md-select>' +
						            '<div ng-messages="form.tipo.$error">' +
						              '<div ng-message="required">Este campo es requerido.</div>' +
						            '</div>' +
						        '</md-input-container>' +
						      '</div>' +
						    '</md-dialog-content>' +
						    '<md-dialog-actions layout="row" ng-if="!cargando">'+
						      '<md-button class=" md-raised red" ng-click="closeDialog()" flex>'+
						        'Cancelar'+
						      '</md-button>'+
						      '<md-button class="md-primary md-raised" type="submit" flex>'+
						        'Guardar'+
						      '</md-button>'+
						    '</md-dialog-actions>'+
						  '</form>'+
						'</md-dialog>',
					controller: 'DialogController',
          clickOutsideToClose:true,
					locals: {
						tipos:$scope.tipos,
						placa: $scope.search,
						placas: $scope.placas,
						info: $scope.info,
						dialogError: $scope.dialogError,
					}
           // Only for -xs, -sm breakpoints.
        })
        .then(function(answer) {
          $scope.status = 'You said the information was "' + answer + '".';
        }, function(a) {
          $scope.status = 'You cancelled the dialog.';
        });
    };
})
.controller('Dialog2Controller', function($scope, $mdDialog, $http, $mdToast, $httpParamSerializer, $timeout, data, servicio, orden, tipo, dialogError){
		$scope.closeDialog = function() {
			  $mdDialog.hide();
		};

		$scope.cargando = false;
		$scope.operarios = data;
		var dataSend = {};
		dataSend.operario = [];

		function selecionarOperario(array) {
			cleanSelect();
			array.forEach(function(item){
				$scope.operarios.forEach(function(operario){
					if (item.id === operario.id) {
						operario.elegido = true;
					}
				});
			});
		}

		$scope.operariosSeleccionados = function(){
			$scope.cargando = true;
			$http({
				'url': '/empleados/operarios/servicio/?q='+ servicio.id,
				'method': 'GET',
			}).then(function doneCallbacks(response){
					selecionarOperario(response.data.object_list);
					$scope.cargando = false;
			},function failCallbacks(response){
				if (response.status == 500) {
						$scope.cargando = false;
						dialogError();
				}else {
					$timeout(function () {
						$scope.operariosSeleccionados();
					}, 2000);
				}
			});
		};

		$scope.operariosSeleccionados();

		function selectCheck(){
			$scope.operarios.forEach(function(item){
				if (item.elegido) {
					dataSend.operario.push(item.id);
				}
			});
		}

		function cleanSelect(){
			$scope.operarios.forEach(function(item){
				item.elegido = false;
			});
		}

		$scope.asignarOperario = function(){
				if(orden){
					$mdDialog.hide();
					$mdToast.show(
						$mdToast.simple()
							.textContent('Guardando...')
							.hideDelay(3000)
							.position('top right')
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
							cleanSelect();
							$mdToast.show(
								$mdToast.simple()
									.textContent('Guardado Exitoso')
					        .hideDelay(3000)
									.position('top right')
							);
					}, function failCallbacks(response){
							if (response.status == 500) {
									dialogError();
							}
					});
				}
		};
})
.controller('DialogController', function($scope, $q, $http, $mdDialog, $mdToast, $httpParamSerializer, placa, placas, tipos, info, dialogError){
		$scope.tipos = tipos;
		$scope.data = {};
		$scope.identificacion = "";
		$scope.celular = "";
		$scope.cargando = false;
		$scope.data.placa = placa;

		$scope.closeDialog = function() {
			  $mdDialog.hide();
		};

		$scope.textChange2 = function(ev) {
				$scope.identificacion = this.search2;
		};

		$scope.textChange3 = function(ev) {
				$scope.celular = this.search3;
		};

		$scope.clienteActual = function(ev) {
			$scope.data.nombre = this.selectedCliente.nombre;
			$scope.data.apellidos = this.selectedCliente.apellidos;
			$scope.data.celular = this.selectedCliente.celular;
			$scope.data.cliente = this.selectedCliente.id;
			$scope.data.identificacion = this.selectedCliente.identificacion;
			console.log($scope.data);
		};

    $scope.listClientes = function(searchText){
			console.log(searchText);
				var deferred = $q.defer();
				if (searchText===undefined) {
					searchText = "";
				}
        $http({
          'url': '/cliente/list/cliente/?q='+ searchText,
          'method': 'GET'
        }).then(function doneCallbacks(response){
						deferred.resolve(response.data.object_list);
        },function failCallbacks(response){
					  deferred.reject(response);
            dialogError();
        });
				return deferred.promise;
    };


		console.log(info);
		$scope.enviar = function(){
			$scope.cargando = true;
			if ($scope.data.cliente) {
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
						info.tipo = result.nombre;
						info.identificacion = $scope.data.identificacion;
						info.nombre = $scope.data.nombre + " " + $scope.data.apellidos;
						info.celular = $scope.data.celular;
						info.marca = $scope.data.marca;
						info.kilometraje = $scope.data.kilometraje;
						info.color = $scope.data.color;
						$mdDialog.hide();
						$mdToast.show(
							$mdToast.simple()
								.textContent('Guardado Exitoso')
				        .hideDelay(3000)
							  .position('top right')
						);
						$scope.cargando = false;
						$scope.data = {};
				}, function failCallbacks(response){
						$scope.cargando = false;
						if (response.status == 400) {
							if (response.data.cliente) {
								$mdToast.show(
									$mdToast.simple()
										.textContent("Cliente: " + response.data.cliente[0])
										.position('top right')
						        .hideDelay(3000)
								);
							}
							if (response.data.placa) {
								$mdToast.show(
									$mdToast.simple()
										.textContent("Placa: " + response.data.placa[0])
										.position('top right')
						        .hideDelay(3000)
								);
							}else if(response.data.tipo){
								$mdToast.show(
									$mdToast.simple()
										.textContent("Tipo: " + response.data.tipo[0])
										.position('top right')
						        .hideDelay(3000)
								);
							}
						}else if (response.status == 500) {
							dialogError();
						}
				});
			} else {
					console.log($scope.identificacion);
					console.log($scope.celular);
					var dataSend = {};
					dataSend.nombre = $scope.data.nombre;
					dataSend.apellidos = $scope.data.apellidos;
					dataSend.identificacion = $scope.identificacion;
					dataSend.celular = $scope.celular;
					dataSend['vehiculo_set-TOTAL_FORMS'] = 3;
					dataSend['vehiculo_set-INITIAL_FORMS'] = 0;
					dataSend['vehiculo_set-MIN_NUM_FORMS'] = 0;
					dataSend['vehiculo_set-MAX_NUM_FORMS'] = 1000;
					dataSend['vehiculo_set-0-placa'] = $scope.data.placa;
					dataSend['vehiculo_set-0-tipo'] = $scope.data.tipo;
					dataSend['vehiculo_set-0-marca'] = $scope.data.marca;
					dataSend['vehiculo_set-0-color'] = $scope.data.color;
					dataSend['vehiculo_set-0-kilometraje'] = $scope.data.kilometraje;
					$http({
						url:'/cliente/add/cliente/inline/',
						method: 'POST',
						data: $httpParamSerializer(dataSend),
					  headers: {
								'Content-Type': 'application/x-www-form-urlencoded'
						},
					}).then(function doneCallbacks(response){
							console.log(response);
							var cliente = response.data;
							var item = {};
							item.placa = $scope.data.placa;
							item.tipo = $scope.data.tipo;
							//hacer busqueda del vehiculo
							function getVehiculo(){
								console.log(item.placa);
								$http({
				          'url': '/cliente/vehiculo/?q='+ item.placa,
				          'method': 'GET'
				        }).then(function doneCallbacks(response){
				            var vehiculo = response.data.object_list;
										item.id = vehiculo[0].id;
										placas.push(item);
										info.tipo = vehiculo[0].tipov;
										info.marca = vehiculo[0].marca;
										info.color = vehiculo[0].color;
										info.kilometraje = vehiculo[0].kilometraje;
										info.identificacion = cliente.identificacion;
										info.nombre = cliente.nombre + " " + cliente.apellidos;
										info.celular = cliente.celular;
										$mdDialog.hide();
										$mdToast.show(
											$mdToast.simple()
												.textContent('Guardado Exitoso')
								        .hideDelay(3000)
											  .position('top right')
										);
										$scope.cargando = false;
										$scope.data = {};
				        },function failCallbacks(response){
				            if(response.status == 500) {
												$scope.cargando = false;
												dialogError();
										}else {
											getVehiculo();
										}
				        });
							}
							getVehiculo();
					}, function failCallbacks(response){
							$scope.cargando = false;
							if (response.status == 400) {
								if (response.data.nombre) {
									$mdToast.show(
										$mdToast.simple()
											.textContent("Nombre: " + response.data.nombre[0])
											.position('top right')
							        .hideDelay(3000)
									);
								}
								if (response.data.apellidos) {
									$mdToast.show(
										$mdToast.simple()
											.textContent("Apellidos: " + response.data.apellidos[0])
											.position('top right')
							        .hideDelay(3000)
									);
								}else if(response.data.identificacion){
									$mdToast.show(
										$mdToast.simple()
											.textContent("Identificación: " + response.data.identificacion[0])
											.position('top right')
							        .hideDelay(3000)
									);
								}
								else if(response.data.celular){
									$mdToast.show(
										$mdToast.simple()
											.textContent("Celular: " + response.data.celular[0])
											.position('top right')
							        .hideDelay(3000)
									);
								}else if (response.data.inlines) {
										var inlines = response.data.inlines;
										inlines.forEach(function(item){
											if (item.placa) {
											$mdToast.simple()
												.textContent("Placa: " + item.placa[0])
												.position('top right')
								        .hideDelay(3000)
											} else if (item.tipo) {
												$mdToast.simple()
													.textContent("Tipo: " + item.tipo[0])
													.position('top right')
									        .hideDelay(3000)
											}
										});
								}
							}else if (response.status == 500) {
									dialogError();
							}
					});
			}
		};
});
