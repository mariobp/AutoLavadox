$(document).on('ready', function(){
  $('.ex-date-filter label:first').text("Por servicios");
  $('.ex-date-filter input[type="submit"]:first').hide();
  $('.export_link').on('click', function(event){
    return false;
  });
  $('.export_link').on('click', function(event){
    var ini = $('#id_drf__nacimiento__gte').val();
    var fin = $('#id_drf__nacimiento__lte').val();
    if(ini.length > 0 && fin.length > 0){
      var r1 = $('#id_drf__nacimiento__gte').val().split("/")
      var r2 = $('#id_drf__nacimiento__lte').val().split("/")
      var f1 = new Date(parseInt(r1[1]), parseInt(r1[0])-1 , parseInt(r1[2]));
      var f2 = new Date(parseInt(r2[1]), parseInt(r2[0])-1 , parseInt(r2[2]));
      if(f2 >f1){
        window.location.href = "http://192.168.2.113:8000/empleados/excel/periodo/?ini="+ini.split("/").join("-")+"&fin="+fin.split("/").join("-");
      }else{
        alert("La fecha de Fin de periodo debe ser mayor, a la de inicio.")
      }
    }else{
      alert("Debe seleccionqr el intervalo de fecha.")
    }

  });
});
