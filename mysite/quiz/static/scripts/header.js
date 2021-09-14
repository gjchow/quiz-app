//function toggleHamburger(x) {
//    x.classList.toggle("change");
//    openNav();
//}
//
//function openNav() {
//    document.getElementById("navbar").addClass("open-sidebar");
//}
//
///* Set the width of the side navigation to 0 */
//function closeNav() {
//    document.getElementById("navbar").style.width = "0";
//}

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