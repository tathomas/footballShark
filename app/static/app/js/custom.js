var nombrePage = $(".bet-content").length;
var currentPage = $("#pagin ul .active").index();
var leftPage = $("#pagin ul .active").index() -1;

showPage = function (pagination) {
    console.log("Current Page:")
    console.log($(this).parent().index());
    if (pagination < 0 || pagination >= nombrePage) return;

    $(".bet-content").hide().eq(pagination).show();
    $("#pagin li").removeClass("active").eq(pagination).addClass("active");
}

// Go to Left
$(".prev").click(function (e) {
    e.preventDefault();
    console.log($("#pagin ul .active").index() - 1);
    showPage($("#pagin ul .active").index() - 1);
});

// Go to Right
$(".next").click(function (e) {
    e.preventDefault();
    showPage($("#pagin ul .active").index() + 1);
});

$("#pagin ul a").click(function (e) {
    e.preventDefault();
    showPage($(this).parent().index());
});

showPage(0)