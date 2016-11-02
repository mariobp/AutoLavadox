$(document).on('ready', function(){
  $('.ex-date-filter label:first').text("Por servicios");
  $('.ex-date-filter input[type="submit"]:first').hide();
  $('.export_link').on('click', function(event){
    return false;
  });
});
