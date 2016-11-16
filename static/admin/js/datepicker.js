$(document).ready(function() {
  $(".date").Zebra_DatePicker({
    format:'m/d/Y',
    lang_clear_date: 'Borrar Fecha',
    show_select_today: 'Hoy',
    default_position: 'below',
    days: ['Domingo', 'Lunes', 'Marte', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'],
    months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiemnbre', 'Octubre', 'Nobiembre', 'Diciembre']
  });
});
