(function($) {
    'use strict';
    function close_menu() {
        $('li.menu').removeClass('activate');
        $('li.menu ul').slideUp('slow').addClass('close');
    }
    function assistant(prefix) {
        if (prefix === undefined){
            prefix = 'form';
        }
        $(".assistant.box").not('.close').addClass('close');
        $('.assistant.box[data-assistant="'+prefix+'"]').removeClass('close');
    }
    $(document).ready(function() {
        $('li.menu > span').click(function(e) {
            if ($(e.currentTarget.parentNode).is('.activate')) {
                close_menu();
            } else {
                close_menu();
                $(e.currentTarget.parentNode).addClass('activate');
                $(e.currentTarget.parentNode).find('ul').slideDown('slow').removeClass('close');
            }
            e.preventDefault();
        });

        // filter.html
        $('.campo select').change(function(e) {
            var href = $(this).find('option:selected').attr('href');
            window.location = window.location.pathname + href;
        });
        //from
        if(/.*\/(change|add)\//g.exec(window.location) !== null){
            if(window.location.hash === ""){
                $(".assistant.box").not('[data-assistant="form"]').addClass('close');
            }else{
                $(".assistant.box").not('[data-assistant="'+window.location.hash.split('#')[1]+'"]').addClass('close');
            }

            $('button.assistant').click(function (e) {
                var prefix = $(this).attr('data-assistant');
                window.location.hash = '#'+prefix;
                assistant(prefix);
                e.preventDefault();
            });

            $(window).on('hashchange', function(){
                assistant(window.location.hash.split('#')[1]);
            });
        }
    });
})(django.jQuery);
