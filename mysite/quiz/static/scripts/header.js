$(document).ready(function(){
    $(".hamburger").click(function(){
        $(".hamburger").toggleClass("change");
        if ($(".sidebar").hasClass("open-sidebar")){
            $(".sidebar").removeClass("open-sidebar");
        } else {
            $(".sidebar").addClass("open-sidebar");
        }
    });
});