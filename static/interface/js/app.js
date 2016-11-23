angular.module('App', ['ngMaterial', 'ngMessages'])
.run(function($window, $rootScope) {
      $rootScope.online = navigator.onLine;
      $window.addEventListener("offline", function() {
        $rootScope.$apply(function() {
          $rootScope.online = false;
        });
      }, false);

      $window.addEventListener("online", function() {
        $rootScope.$apply(function() {
          $rootScope.online = true;
        });
      }, false);
})
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
      if ($scope.cerrar) {
          $window.opener = null;
          $window.close();
         return true;
      } else {
         var con = confirm("Are you sure you want to navigate away from this page");
         if (con) {
            return con;
         } else {
           $scope.cerrar = false;
           return false;
         }
      }
	  };
    $scope.cerrar = false;
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
    $scope.habilitarObservacion = true;
    $scope.cancelarOrden = true;
		$scope.bandera = false;
    $scope.editarVehiculo = true;
		$scope.serv1 = false;
		$scope.serv2 = false;
		$scope.serv3 = false;
		$scope.serv4 = false;
		$scope.serv5 = false;
		$scope.serv6 = false;
		$scope.serv7 = false;
    $scope.serv8 = false;
		$scope.dialogOpen = false;
		var data = {};


		$scope.$watch('online', function(newStatus) {
				if (newStatus) {
	        if ($scope.bandera) {
						$mdToast.show(
							$mdToast.simple()
								.textContent('Internet Ok....')
								.hideDelay(3000)
								.position('top right')
						);
	        }
				}else {
						$mdToast.show(
							$mdToast.simple()
								.textContent('Sin internet....')
								.hideDelay(3000)
								.position('top right')
						);
	          $scope.bandera = true;
				}
		});

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
      console.log("entro");
      var confirm = $mdDialog.confirm()
      .title('Estas seguro que quieres cerrar la sesión?')
      .ariaLabel('Sesion')
      .ok('Si')
      .cancel('No');
      $mdDialog.show(confirm).then(function() {
          $scope.cerrar = true;
          $http({
            'url': '/empleados/logout/',
            'method': 'GET',
          }).then(function doneCallbacks(response){
              location.href = "/empleados/login/";
          }, function failCallbacks(response){
              $scope.dialogError();
          });
      }, function() {

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

		function informacion(selectedItem){
			if (selectedItem.nombre && selectedItem.apellidos ) {
				$scope.info.nombre = selectedItem.nombre + " " + selectedItem.apellidos;
			}
			if (selectedItem.color) {
				$scope.info.color = selectedItem.color;
			}if (selectedItem.marca) {
				$scope.info.marca = selectedItem.marca;
			}if (selectedItem.kilometraje) {
				$scope.info.kilometraje = selectedItem.kilometraje;
			}
			$scope.info.celular = selectedItem.celular;
			$scope.info.identificacion = selectedItem.cedula;
			$scope.info.tipo = selectedItem.tipo;
      $scope.info.placa = selectedItem.placa;
      $scope.info.id = selectedItem.id;
      $scope.editarVehiculo = false;
		}

		//Vehiculo seleccionado
    $scope.vehiculoActual = function($event){
			function placaRepetida(vehiculo) {
					return vehiculo.placa === $scope.selectedItem.placa;
			}
      if ($scope.selectedItem) {
					informacion($scope.selectedItem);
          if (!$scope.placas.includes($scope.selectedItem)) {
							var result = $scope.placas.find(placaRepetida);
						if (result === undefined) {
						   $scope.placas.push($scope.selectedItem);
			 				 $scope.selectedPlaca = $scope.selectedItem;
 							 $scope.serviciosList();
						}else {
							if (result.ordenv) {
                  $scope.selectedPlaca = result;
				          $scope.serviciosList();
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
          $scope.info.id = "";
          $scope.info.placa = "";
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

    //Funcion que se llama cuando se selecciona otra placa en la lista de servicios
    $scope.placaChange = function(){
      $scope.cancelarOrden = true;
    	informacion($scope.selectedPlaca);
      $scope.serviciosList();
    };

		//Lista de servicios aplicables
		$scope.serviciosList = function(){
        habilitar3();
				function porasignar() {
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
							$scope.serv6 = false;
							if (response.status == 500) {
								$scope.dialogError();
							}
					});
				}
				if (!$scope.selectedPlaca.ordenv) {
					$scope.serv5 = true;
					$scope.serv6 = true;
					$scope.serviciosPorHacer = [];
					$http({
						'url': '/operacion/ws/tipo/servicio/?q='+ $scope.selectedPlaca.tipo,
						'method': 'GET',
					}).then(function doneCallbacks(response){
							$scope.servicios = response.data.object_list;
							$scope.serv5 = false;
							$scope.serv6 = false;
              habilitar2();
              valor($scope.serviciosPorHacer);
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
              porasignar();
							habilitar();
              habilitar2();
					}, function failCallbacks(response){
							$scope.serv5 = false;
            	$scope.serv6 = false;
							$scope.dialogError();
					});
				}
		};

		function valor(array){
			$scope.totalService = 0;
			array.forEach(function(item){
				if (item.status) {
					$scope.totalService+= item.costo;
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
            habilitar2();
						$mdToast.show(
							$mdToast.simple()
								.textContent('Guardado Exitoso')
								.hideDelay(3000)
								.position('bottom right')
						);
				}, function failCallbacks(response){
						if (response.status == 500) {
								$scope.dialogError();
						}
				});
		}


		$scope.changeCheck = function (servicio) {
      habilitar3();
			if(servicio.status){
			  var confirm = $mdDialog.confirm()
	      .title('Estas seguro que quieres cancelar?')
	      .ariaLabel('Lucky day')
	      .ok('Si')
	      .cancel('No');
				$mdDialog.show(confirm).then(function() {
					$scope.serv5 = true;
					$scope.serv6 = true;
        	valor($scope.serviciosPorHacer);
					$http({
						'url':'/operacion/cancel/servicio/'+servicio.id+'/',
						'method': 'GET'
					}).then(function doneCallbacks(response){
							$scope.serv5 = false;
							$scope.serv6 = false;
							servicio.status = !servicio.status;
							removeFromArray($scope.serviciosPorHacer, servicio);
              habilitar2();
							valor($scope.serviciosPorHacer);
							$mdToast.show(
								$mdToast.simple()
									.textContent('Servicio cancelado')
					        .hideDelay(3000)
									.position('bottom right')
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
                	valor($scope.serviciosPorHacer);
                  habilitar2();
									registrarServicio(data, servicio);
										$mdToast.show(
											$mdToast.simple()
												.textContent('Servicio asignado')
								        .hideDelay(3000)
												.position('bottom right')
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

    //Habilita o desabilita el boton de cerrar orden, siempre y cuando todos los servicios por hacer esten listos
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

    //Habilita o desabilita el boton de cancelar orden, siempre y cuando no tenga ningun servicio asignano
		function habilitar2(){
				var n = $scope.servicios.length;
				if (n > 0) {
					$scope.servicios.forEach(function(item){
							if(!item.status){
								n = n - 1;
							}
					});
					if(n===0){
						$scope.cancelarOrden = false;
					}else {
						$scope.cancelarOrden = true;
					}
				}else {
					$scope.cancelarOrden = false;
				}
		}

    //Habilita o desabilita el boton de agregar observacion, siempre y cuando se cree una orden
    function habilitar3(){
      if ($scope.selectedPlaca.ordenv) {
        $scope.habilitarObservacion = false;
      }else {
        $scope.habilitarObservacion = true;
      }
    }

    $scope.cancelado = function() {
        if (!$scope.selectedPlaca.ordenv) {
          	$scope.servicios = [];
            removeFromArray($scope.placas, $scope.selectedPlaca);
        		$mdToast.show(
							$mdToast.simple()
								.textContent('Cancelado Exitoso')
				        .hideDelay(3000)
							  .position('bottom right')
						);
            $scope.cancelarOrden = true;
        }else {
            var confirm = $mdDialog.confirm()
    	      .title('Estas seguro que quieres cancelar la Orden?')
    				.textContent('No se podra modificar una vez se cancele.')
    	      .ariaLabel('DD')
    	      .ok('Si')
    	      .cancel('Cancelar');
    				$mdDialog.show(confirm).then(function() {
              $scope.serv6 = true;
    					$scope.serv7 = true;
    					$http({
    						'url': '/operacion/cancelar/orden/'+$scope.selectedPlaca.ordenv,
    						'method': 'GET'
    					}).then(function doneCallbacks(response){
    							$scope.servicios = [];
    							$scope.serviciosPorHacer = [];
                  removeFromArray($scope.placas, $scope.selectedPlaca);
    							valor($scope.serviciosPorHacer);
    							$mdToast.show(
    								$mdToast.simple()
    									.textContent('Cancelado Exitoso')
    					        .hideDelay(3000)
    									.position('bottom right')
    							);
    							$scope.serv6 = false;
    							$scope.serv7 = false;
                  $scope.cancelarOrden = true;
    					},function failCallbacks(response){
    							if (response.status == 500) {
    									$scope.dialogError();
    							}
    					});
    				}, function() {

    				});
        }
    };

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
								.position('bottom right')
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

        function enviar(){
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
									.position('bottom right')
							);
							$scope.serv6 = false;
							$scope.serv7 = false;
					},function failCallbacks(response){
							if (response.status == 500) {
									$scope.dialogError();
							}
					});
        }

			  var confirm = $mdDialog.confirm()
	      .title('Estas seguro que quieres cerrar la Orden?')
				.textContent('No se podra modificar una vez se cierre.')
	      .ariaLabel('DD')
	      .ok('Si')
	      .cancel('Cancelar');
				$mdDialog.show(confirm).then(function() {
          enviar();
				}, function() {

				});

		};

    //Actualizar vehiculos
    $scope.actualizarVehiculo = function() {
        var data = {};
        data.placa = $scope.info.placa;
        data.color = $scope.info.color;
        data.marca = $scope.info.marca;
        data.kilometraje = $scope.info.kilometraje;
        data.tipo = $scope.info.tipo;
        $scope.serv8 = true;
        $http({
					url:'/cliente/edit/vehiculo/'+$scope.info.id+'/',
					method: 'POST',
					data: $httpParamSerializer(data),
				  headers: {
							'Content-Type': 'application/x-www-form-urlencoded'
					},
				}).then(function doneCallbacks(response){
            $scope.tipochange();
						$mdToast.show(
							$mdToast.simple()
								.textContent('Actualizado Exitoso')
				        .hideDelay(3000)
							  .position('top right')
						);
						$scope.serv8 = false;
				}, function failCallbacks(response){
						$scope.serv8 = false;
						if (response.status == 400) {
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
    };

    //Cambio de tipo

    $scope.tipochange = function(){
      $scope.selectedPlaca.tipo = $scope.info.tipo;
      $scope.serviciosList();
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
						      '<div class="md-dialog-content" ng-hide="cargando">' +
									'<div layout="row">' +
		                '<md-autocomplete md-input-name="celular" md-input-minlength="7"	md-input-maxlength="20" md-floating-label="Celular" md-no-float md-selected-item="selectedCliente" md-no-cache="true" md-min-length="0" md-selected-item-change="clienteActual($event)"	md-search-text-change="textChange3(search3)" md-search-text="search3" md-items="cliente in listClientes(search3)" md-item-text="cliente.celular" placeholder="Escribir el numero de celular" flex required>' +
                      '<md-item-template>' +
                        '<span md-highlight-text="search">[[cliente.nombre]] [[cliente.apellidos]] - [[cliente.celular]]</span>' +
                      '</md-item-template>' +
                      '<md-not-found>' +
												'No hay hay resultados para "[[search3]]"' +
											'</md-not-found>' +
											'<div ng-messages="form.celular.$error">' +
												'<div ng-message="required">Este campo es requerido.</div>' +
                        '<div ng-message="minlength">Este campo no debe tener menos de 7 digitos.</div>' +
                        '<div ng-message="maxlength">Este campo no debe superar los 20 digitos.</div>' +
											'</div>' +
										'</md-autocomplete >' +
		              '</div>' +
									'<div layout="row">' +
		                '<md-autocomplete md-input-name="identificacion" md-input-minlength="7" md-input-maxlength="20" md-floating-label="Identificación" md-no-float md-selected-item="selectedCliente" md-no-cache="true" md-min-length="0" md-selected-item-change="clienteActual($event)"	md-search-text-change="textChange2(search2)" md-search-text="search2" md-items="cliente in listClientes(search2)" md-item-text="cliente.identificacion" placeholder="Escribir el numero de identificación" flex>' +
                      '<md-item-template>' +
                          '<span md-highlight-text="search">[[cliente.nombre]] [[cliente.apellidos]] - [[cliente.identificacion]]</span>' +
                      '</md-item-template>' +
                       '<md-not-found>' +
												'No hay hay resultados para "[[search2]]"' +
											'</md-not-found>' +
											'<div ng-messages="form.identificacion.$error">' +
												'<div ng-message="required">Este campo es requerido.</div>' +
                        '<div ng-message="minlength">Este campo no debe tener menos de 7 digitos.</div>' +
                        '<div ng-message="maxlength">Este campo no debe superar los 20 digitos.</div>' +
											'</div>' +
										'</md-autocomplete >' +
		              '</div>' +
		              '<div layout="row">' +
		                '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100" >' +
		                   '<label>Nombre</label>' +
		                    '<input type="text" ng-model="data.nombre" name="nombre" value="" >' +
		                    '<div ng-messages="form.nombre.$error">' +
		                      '<div ng-message="required">Este campo es requerido.</div>' +
		                    '</div>' +
		                '</md-input-container>' +
		                '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100" >' +
		                   '<label>Apellidos</label>' +
		                    '<input type="text" ng-model="data.apellidos" name="apellidos" value="" >' +
		                    '<div ng-messages="form.apellidos.$error">' +
		                      '<div ng-message="required">Este campo es requerido.</div>' +
		                    '</div>' +
		                '</md-input-container>' +
		              '</div>' +
										'<div layout="row">' +
			                  '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
			                    '<label>Placa</label>' +
			                    '<input ng-model="data.placa" name="placa" required>' +
			                    '<div ng-messages="form.placa.$error">' +
			                      '<div ng-message="required">Este campo es requerido.</div>' +
			                    '</div>' +
			                  '</md-input-container>' +
									      '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
								          '<label>Marca</label>' +
								          '<input ng-model="data.marca" name="marca">' +
								          '<div ng-messages="form.marca.$error">' +
								            '<div ng-message="required">Este campo es requerido.</div>' +
								          '</div>' +
								        '</md-input-container>' +
			              '</div>' +
										'<div layout="row">' +
											'<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
												'<label>Color</label>' +
												'<input ng-model="data.color" name="color">' +
												'<div ng-messages="form.color.$error">' +
													'<div ng-message="required">Este campo es requerido.</div>' +
												'</div>' +
											'</md-input-container>' +
											'<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
												'<label>Kilometraje</label>' +
												'<input ng-model="data.kilometraje" name="kilometraje">' +
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
					fullscreen: true,
					onComplete: function(scope, element){
							var elemento = document.querySelector(".md-dialog-container");
              if (elemento) {
                elemento.style.zIndex=80;
              }
					},
					parent: angular.element(document.querySelector('#popupContainer')),
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
						var elemento = document.querySelector(".md-dialog-container");
            if (elemento) {
              elemento.style.zIndex=101;
            }
          $scope.status = 'You said the information was "' + answer + '".';
        }, function(a) {
					var elemento = document.querySelector(".md-dialog-container");
          if (elemento) {
            elemento.style.zIndex=101;
          }
          $scope.status = 'You cancelled the dialog.';
        });
    };

    $scope.agregarObservacion = function(ev){
        var dialog = $mdDialog.show({
          template:
          '<md-dialog aria-label="observacion">' +
            '<form ng-cloak name="form" ng-submit="form.$valid && guardar()" novalidate>' +
              '<md-toolbar>' +
                '<div class="md-toolbar-tools">' +
                  '<h2>Observación</h2>' +
                  '<span flex></span>' +
                '</div>' +
              '</md-toolbar>' +
              '<md-dialog-content>' +
            		'<div layout="row" layout-align="center center" ng-if="cargando2" style="height:300px">' +
					  				'<md-progress-circular ng-disabled="!cargando2" md-mode="indeterminate" md-diameter="50"></md-progress-circular>' +
					  		'</div>' +
                '<div class="md-dialog-content" ng-if="!cargando2">' +
                  '<md-input-container class="md-block" flex="50" flex-xs="100" flex-gt-sm="100">' +
                    '<label>Observación</label>' +
                    '<textarea ng-model="data.observacion" name="observacion"  md-maxlength="500" rows="5" required>' +
                    '</textarea>' +
                    '<div ng-messages="form.observacion.$error">' +
                      '<div ng-message="required">Este campo es requerido.</div>' +
                    '</div>' +
                  '</md-input-container>' +
                '</div>'+
              '</md-dialog-content>'+
              '<md-dialog-actions layout="row" ng-if="!cargando2">'+
                '<md-button class="md-raised red" ng-click="closeDialog()" flex>'+
                  'Cancelar'+
                '</md-button>'+
                '<md-button class="md-primary md-raised" type="submit" flex>'+
                  'Guardar'+
                '</md-button>'+
              '</md-dialog-actions>'+
            '</form>'+
          '</md-dialog>',
          controller: 'Dialog3Controller',
          locals: {
            orden: $scope.selectedPlaca.ordenv,
            dialogError: $scope.dialogError,
          },
          clickOutsideToClose:true,
          parent: angular.element(document.querySelector('#popupContainer')),
          targetEvent: ev,
        }).then(function(){

        },function(){

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
							.position('bottom right')
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
									.position('bottom right')
							);
					}, function failCallbacks(response){
							if (response.status == 500) {
									dialogError();
							}
					});
				}
		};
})

.controller('Dialog3Controller', function($scope, $mdDialog, $http, $httpParamSerializer, $mdToast, orden, dialogError){
    $scope.data = {};
    $scope.closeDialog = function() {
			  $mdDialog.hide();
		};
    $scope.cargando2 = false;

    $scope.single = function() {
        $scope.cargando2 = true;
				$http({
					'url':'/operacion/list/orden/?q='+orden,
					'method': 'GET'
				}).then(function doneCallbacks(response){
						$scope.data.observacion = response.data.object_list[0].observacion;
            $scope.cargando2 = false;
				}, function failCallbacks(response){
            $scope.cargando2 = false;
						if (response.status == 500) {
								$scope.dialogError();
						}
				});
    };

    $scope.single();

    $scope.guardar = function() {
        $scope.cargando2 = true;
       	$http({
           'url': '/operacion/edit/observacion/'+ orden +'/',
            'method': 'POST',
            'data': $httpParamSerializer($scope.data),
             headers: {
                 'Content-Type': 'application/x-www-form-urlencoded'
             },
         }).then(function doneCallbacks(response){
             $mdDialog.hide();
             $scope.cargando2 = false;
             $mdToast.show(
               $mdToast.simple()
                 .textContent('Observación guardada')
                 .hideDelay(3000)
                 .position('bottom right')
             );
         }, function failCallbacks(response){
             $scope.cargando2 = false;
             if (response.status == 500) {
                 dialogError();
             }
         });
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

		$scope.textChange2 = function(search) {
      console.log(search);
				$scope.identificacion = search;
		};

		$scope.textChange3 = function(search) {
      console.log(search);
				$scope.celular = search;
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
            info.id = response.data.id;
            info.placa = response.data.placa;
						info.tipo = result.id;
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
                    info.id = vehiculo[0].id;
                    info.placa = vehiculo[0].placa;
										info.tipo = vehiculo[0].tipo;
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
								        .hideDelay(3000);
											} else if (item.tipo) {
												$mdToast.simple()
													.textContent("Tipo: " + item.tipo[0])
													.position('top right')
									        .hideDelay(3000);
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
