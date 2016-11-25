$(document).on('ready', function(){
  console.log('ready');
  $('.ex-date-filter label:first').text("Rango de analisis");
  $('.ex-date-filter input[type="submit"]:first').val("Servicios");
  $('.ex-date-filter input[type="submit"]:first').parent().prepend("<input type=\"submit\" class=\"comision\" value=\"Comisión\">");
  $('.ex-date-filter input[type="submit"]:first, .comision').on('click', function(event){
    return false;
  });

  $('.ex-date-filter input[type="submit"]:first').on('click', function(event){
    var ini = $('#id_drf__nacimiento__gte').val();
    var fin = $('#id_drf__nacimiento__lte').val();
    if(ini.length > 0 && fin.length > 0){
      var r1 = ini.split("/")
      var r2 = fin.split("/")
      var f1 = new Date(parseInt(r1[1]), parseInt(r1[0])-1 , parseInt(r1[2]));
      var f2 = new Date(parseInt(r2[1]), parseInt(r2[0])-1 , parseInt(r2[2]));
      console.log(f2 >f1);
      if(f2 >f1){
        var d1 = r1[2]+"-"+r1[0]+"-"+r1[1];
        var d2 = r2[2]+"-"+r2[0]+"-"+r2[1];
        console.log(d1,d2);
        window.location.href = "/empleados/excel/empleados/?ini="+d1+"&fin="+d2;
      }else{
        alert("La fecha de Fin de periodo debe ser mayor, a la de inicio.")
      }
    }else{
      alert("Debe seleccionar el rango de fechas");
    }
  });
  $('.comision').on('click', function(event){
    var ini = $('#id_drf__nacimiento__gte').val();
    var fin = $('#id_drf__nacimiento__lte').val();
    if(ini.length > 0 && fin.length > 0){
      var r1 = ini.split("/")
      var r2 = fin.split("/")
      var f1 = new Date(parseInt(r1[1]), parseInt(r1[0])-1 , parseInt(r1[2]));
      var f2 = new Date(parseInt(r2[1]), parseInt(r2[0])-1 , parseInt(r2[2]));
      console.log(f2 >f1);
      if(f2 >f1){
        var d1 = r1[2]+"-"+r1[0]+"-"+r1[1];
        var d2 = r2[2]+"-"+r2[0]+"-"+r2[1];
        console.log(d1,d2);
        window.location.href = "/empleados/report/comi/?ini="+d1+"&fin="+d2;
      }else{
        alert("La fecha de Fin de periodo debe ser mayor, a la de inicio.")
      }
    }else{
      alert("Debe seleccionar el rango de fechas");
    }
  });
});
