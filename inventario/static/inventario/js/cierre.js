$(document).on('ready',function(){
    $('.imprimir').on('click', function(){
        return false;
    });
    $('.imprimir').on('click', function(){
        window.open($(this).attr('href'),'_blank');
    });
});
