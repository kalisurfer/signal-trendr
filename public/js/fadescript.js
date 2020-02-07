/*
 Fadescript inspired and grabed in whole or part from http://roybarber.com/
*/

function newpage() {
    window.location = newLocation
}

function Reload() {
    try {
        var e = document.getElementsByTagName("head")[0];
        e && e.innerHTML && (e.innerHTML += " ")
    } catch (t) {}
}
/iphone|ipod|ipad.*os 5/gi.test(navigator.appVersion) && (window.onpageshow = function (e) {
    if (e.persisted) {
        document.body.style.display = "none";
        location.reload()
    }
});
$(document).ready(function () {
    $("body").css("display", "none");
    $.fn.collapsable = function (e) {
        return this.each(function () {
            var e = $(this),
                t = $(".main");
            /*
            e.click(function () {
                if (e.is(":visible")) {
                    t.slideToggle("fast");
                    t.toggleClass("clearfix")
                }
            }); 
            $(window).resize(function () {
                $(window).width() >= 600 && t.toggleClass("clearfix").show()
            })*/
        })
    };
    var e = $(".menu-btn");
    e.collapsable();
    e.click(function (t) {
        e.toggleClass("open")
    });
    $("body").fadeIn(600);
    $("a[rel=fade]").click(function (e) {
        e.preventDefault();
        newLocation = this.href;
        $("body").fadeOut(600, newpage)
    })
});
window.addEventListener("load", function () {
    setTimeout(function () {
        window.scrollTo(0, 1)
    }, 0)
});

/* function to get pages to fade in and out */
$( "div.title" ).click(function() {
	var divdata = $(this);
	var id = divdata.attr("data-id");

    $.ajax({
      type: 'GET',
      url: '/home/details/' + id,
      /*data: { id },*/
      dataType: 'html',
      success: function(data){
        // Do some nice stuff here
        //alert("foo bar" + data)
        $("div#cardsection").html(data);
        //var ctx = document.getElementById("myChart").getContext("2d");
        //var myNewChart = new Chart(ctx).Line(data, options);
      },
      error: function(xhr, type){
        alert('Y U NO WORK?')
      }
    });
});

/* function to make URLs clickable in returned tweets */
function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    //URLs starting with http://, https://, or ftp://
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');

    //URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    //Change email addresses to mailto:: links.
    replacePattern3 = /(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
}

