$(document).on('ready', function() {
    $('a.imprimir').on('click', function(event) {
        return false;
    });
    $('.imprimir').on('click', function(event) {
      //window.open("/operacion/imprimir/orden/"+$(this).attr('href')+"/", '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes')
        $.ajax({
            url: "/operacion/get/info/orden/?orden_id="+$(this).attr('href'),
            type: 'get',
            dataType: 'json',
            success: function(data) {
              $.ajax({
                  url:'http://127.0.0.1:9004/printp',
                  contentType: 'application/json; charset=utf-8',
                  dataType:'text',
                  method:'post',
                  data: JSON.stringify(data),
                  success:function(datas){
                    console.log(datas);
                  }
                });
            }
        });
    });
});
