$(document).ready(function(){
    const ans = JSON.parse(document.getElementById('ans').textContent);
    console.log(ans)
    $(".button").click(function(){
        $(".button").prop("disabled", true);
        $(".button").addClass("disable");
        $("#"+ans).addClass("correct");
        setTimeout(
            function(){
                $("#question-form").submit();
            }, 1000);
        });
});