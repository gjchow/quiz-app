$(document).ready(function(){
    $('#add_more').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        if (form_idx < 10){
            $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        };
    });
});