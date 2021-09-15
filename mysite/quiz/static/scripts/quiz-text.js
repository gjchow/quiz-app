$(document).ready(function(){
    const ans = JSON.parse(document.getElementById('ans').textContent);
    $("#form1").submit(function(e){
        $(".text-ans").addClass("disable");
        $(".text-ans").prop("disabled", true);
        if ($(".text-ans").val() != ans){
            $(".text-ans").addClass("wrong");
            $(".text-ans").val(ans);
        } else {
            $(".text-ans").addClass("correct");
        }
        e.preventDefault();
        setTimeout(
            function(){
               $("#form1").unbind("submit").submit();
            }, 1000);
        });
});