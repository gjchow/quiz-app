$(document).ready(function(){
    $(':input[type=text]').removeClass('text-ans');
    $(':input[type=text]').addClass('text-disabled');
    $(':input[type=text]').prop('disabled', true);
    $('#edit').click(function(){
        $(':input[type=text]').toggleClass('text-ans');
        $(':input[type=text]').toggleClass('text-disabled');
        $(':input[type=text]').prop('disabled', function(i, v) { return !v; });
        $('#edit').toggle();
        $('#delete').toggle();
        $('#save').toggle();
        $('#cancel').toggle();
    });
    $('#save').click(function(){
        $(':input[type=text]').toggleClass('text-ans');
        $(':input[type=text]').toggleClass('text-disabled');
        $(':input[type=text]').prop('disabled', function(i, v) { return !v; });
        $('#edit').toggle();
        $('#delete').toggle();
        $('#save').toggle();
        $('#cancel').toggle();
    });
    $('#cancel').click(function(){
        $(':input[type=text]').toggleClass('text-ans');
        $(':input[type=text]').toggleClass('text-disabled');
        $(':input[type=text]').prop('disabled', function(i, v) { return !v; });
        $('#edit').toggle();
        $('#delete').toggle();
        $('#save').toggle();
        $('#cancel').toggle();
    });
});