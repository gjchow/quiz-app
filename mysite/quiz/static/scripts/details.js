$(document).ready(function(){
    $(':input').removeClass('text-ans');
    $(':input').addClass('text-disabled');
    $(":input").prop('disabled', true);
});