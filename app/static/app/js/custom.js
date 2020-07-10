var nombrePage = $(".bet-content").length;
var currentPage = $("#pagin ul .active").index();
var leftPage = $("#pagin ul .active").index() -1;

showPage = function (pagination) {
    if (pagination < 0 || pagination >= nombrePage) return;


    $(".bet-content").hide().eq(pagination).show();
    $("#pagin li").removeClass("active").eq(pagination).addClass("active");

    if (($("#pagin ul .active").index() + 1) < 0 || ($("#pagin ul .active").index() + 1) >= nombrePage) {
        $(".next").attr("disabled", "disabled");
    } else {
        $(".next").removeAttr("disabled");
    }
    if (($("#pagin ul .active").index() - 1) < 0 || ($("#pagin ul .active").index() - 1) >= nombrePage) {
         $(".prev").attr("disabled", "disabled");
    }
    else {
        $(".prev").removeAttr("disabled");
    }
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