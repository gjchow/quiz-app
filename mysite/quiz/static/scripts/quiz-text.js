$(document).ready(function(){
    const ans = JSON.parse(document.getElementById('ans').textContent);
    $("#form1").submit(function(e){
        form1 = this;
        $(".text-ans").addClass("disable");
        $(".text-ans").prop("disabled", true);
        $("#real-ans").val($(".text-ans").val());
        if ($(".text-ans").val() != ans){
            $(".text-ans").addClass("wrong");
            $(".text-ans").val(ans);
        } else {
            $(".text-ans").addClass("correct");
        }
        e.preventDefault();
        setTimeout(
            function(){
               $(".text-ans").prop("disabled", false);
               form1.submit();
            }, 1000);
        });
});