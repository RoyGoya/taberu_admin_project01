$(document).ready(function () {
    var _common = $.taberu.common,
        _url = $.taberu.url,
        _mTestEle = $( "div#box-mtest" ),
        _mResultEle = $( "div#box-mresult");

    _mTestEle.on("click", "li.bt-get",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "li.bt-get" )) {
                var _loadingEle = "<div class='loading'>\n" +
                    "<img src='static/img/loading.gif'>\n" +
                    "</div>";

                if (_mResultEle.is(".off")) {
                    _mResultEle.append(_loadingEle);
                    _mResultEle.show();
                    _mResultEle.removeClass("off").addClass("on");
                } else if (_mResultEle.is(".on")) {
                    _mResultEle.empty();
                    _mResultEle.append(_loadingEle);
                }
                $.get(_url.api.medicationOpen, function (data) {
                    _mResultEle.empty();
                    _mResultEle.append(data);
                })
            }

        });

});