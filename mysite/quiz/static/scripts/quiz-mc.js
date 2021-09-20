$(document).ready(function(){
    const ans = JSON.parse(document.getElementById('ans').textContent);
    $(".button").click(function(){
        $(".button").addClass("disable");
        $(".button").prop("disabled", true);
        if (this.id != ans){
            $("#"+this.id).addClass("wrong");
        }
        $("#"+ans).addClass("correct");
        $("#real-ans").val(this.value);
        $("#correct-ans").val($("#"+ans).val())
        setTimeout(
            function(){
               $("#question-form").submit();
            }, 1000);
        });
});