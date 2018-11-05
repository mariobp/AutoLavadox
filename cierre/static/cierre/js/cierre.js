$(document).on('ready',function(){
    $('a.generar.addlink').on('click', function(){
        return false;
    });
    $('a.generar.addlink').on('click', function(){
        window.open($(this).attr('href'),'_blank');
    });
});
