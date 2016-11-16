$(document).on('ready', function() {
    $('a.imprimir').on('click', function(event) {
        return false;
    });
    $('.imprimir').on('click', function(event) {
      window.open("/operacion/imprimir/orden/"+$(this).attr('href')+"/", '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes')
        /*$.ajax({
            url: '/operacion/ws/imprimir/orden/?q=1',
            type: 'get',
            dataType: 'json',
            success: function(data) {
                console.log(data);
                var res = "<table width=\"50%\">",
                    r = "";
                res += "<tr><th width=\"70%\">SERVICIOS AUTOMOVILES</th><th width=\"30%\">VALOR UNITARIO</th></tr>";
                var d = data.object_list;
                window.ra =data;
                for (var i = 0; i < d.length; i++) {
                    if (i == 0) {
                        r += "<ul>";
                        r += "<li>Orden : " + d[i].orden_id + "</li>";
                        r += "<li>Cliente : " + d[i].nombre +" " + d[i].apellidos + "</li>";
                        r += "<li>Identificacion : " + d[i].identificacion + "</li>";
                        r += "<li>Placa : " + d[i].placa + "</li>";
                        res = "</ul>";
                    }
                    res += "<tr><td>" + d[i].servicio + "</td><td>$ " + d[i].costo + "</td></tr>";
                }
                var printContents = r+res;
                var originalContents = document.body.innerHTML;
                document.body.innerHTML = printContents;
                window.print();
                document.body.innerHTML = originalContents;
            }
        });*/
    });
});
