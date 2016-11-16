$(document).on('ready',function(){
  console.log("jajaja");
  $('.ex-date-filter label:first').text("Reporte Servicio mas demorado");
  $('.ex-date-filter input[type="submit"]:first').val('Generar');
  $('.ex-date-filter input[type="submit"]:first').on('click',function(event){return false;});
  $('.ex-date-filter input[type="submit"]:first').on('click',function(event){
    var ini = $('#id_drf__inicio__gte').val();
    var fin = $('#id_drf__inicio__lte').val();
    if(ini.length > 0 && fin.length > 0){
      var r1 = ini.split("/")
      var r2 = fin.split("/")
      var f1 = new Date(parseInt(r1[1]), parseInt(r1[0])-1 , parseInt(r1[2]));
      var f2 = new Date(parseInt(r2[1]), parseInt(r2[0])-1 , parseInt(r2[2]));
      console.log(f2 >f1);
      if(f2 >f1){
        window.location.href = "/operacion/generar/excel/mservicio/";
        console.log("llego aca");
        }else{
          alert("La fecha de Fin de periodo debe ser mayor, a la de inicio.")
          console.log("La fecha de Fin de periodo debe ser mayor, a la de inicio.")
        }
      }else{
        alert("Debe seleccionar el rango de fechas");
        console.log("Debe seleccionar el rango de fechas");
      }
    });
});
