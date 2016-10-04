// This awesome jQuery plugin is developed by balintsoos. https://github.com/balintsoos/material-ripple
(function($) {
    $(document).ready(function() {
        $(".mripple").click(function(event) {
            var surface = $(this);

            if (surface.find(".mink").length === 0) {
                surface.prepend("<div class='mink'></div>");
            }

            var ink = surface.find(".mink");
            ink.removeClass("animate");

            if (!ink.height() && !ink.width()) {
                var d = Math.max(surface.outerWidth(), surface.outerHeight());
                ink.css({
                    height: d,
                    width: d
                });
            }

            var x = event.pageX - surface.offset().left - (ink.width() / 2);
            var y = event.pageY - surface.offset().top - (ink.height() / 2);
            var rippleColor = surface.data("ripple-color");

            ink.css({
                top: y + 'px',
                left: x + 'px',
                background: rippleColor
            }).addClass("animate");
        });
    });
})(django.jQuery);
