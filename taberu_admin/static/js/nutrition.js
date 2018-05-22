$(document).ready(function () {

    /*
 Module Pattern
     https://learn.jquery.com/code-organization/concepts/
*/
    var _nutrition = $.taberu.nutrition,
        _url = $.taberu.url;

    // Jquery Custom Events
    // https://learn.jquery.com/events/introduction-to-custom-events/
    $( "li#box-ndetail" ).on("click", "ul#dt_pattern > li > input, " +
        "ul#pattern1 > li > input, ul#pattern2 > li > input",
        function ( e) {
            var _currentEle = $( this ),
                _dtPatternEle = $( "ul#dt_pattern" ),
                _pattern1Ele = $( "ul#pattern1" ),
                _pattern2Ele = $( "ul#pattern2" ),
                _nlistEle = $( "li#box-nlist" );

            if ( _currentEle.is( "ul#dt_pattern > li > input" ) ) {
                var _dtPatternVal = _currentEle.val(),
                    _dtInputs = $( "ul#dt_pattern").find( "input" ),
                    _ntInputs = $( "ul#pattern1" ).find( "input" ),
                    _paramData = $.param({ dt_pattern: _dtPatternVal});
                _nutrition.clearCheckedInputEls(_dtInputs);
                _currentEle.prop("checked", true);
                _nutrition.clearCheckedInputEls(_ntInputs);
                _pattern2Ele.empty();
                _nutrition.loadTemplate(_url.nutrition.list, _nlistEle,
                    _paramData);

            } else if ( _currentEle.is( "ul#pattern1 > li > input" ) ) {
                var _dtPatternVal = _dtPatternEle.find( "input:checked" ).val(),
                    _pattern1Val = _currentEle.val(),
                    _pattern1Inputs = _pattern1Ele.find( "input" ),
                    _paramData = $.param({
                        dt_pattern: _dtPatternVal,
                        pattern1: _pattern1Val
                    });
                _nutrition.clearCheckedInputEls(_pattern1Inputs);
                _currentEle.prop("checked", true);
                _nutrition.loadTemplate(_url.nutrition.list, _nlistEle,
                    _paramData);
                _nutrition.getNutritionPattern2(_url.nutrition.pattern2,
                    _pattern1Val);

            } else if ( _currentEle.is( "ul#pattern2 > li > input" ) ) {
                console.log("pattern2");

            }
        });

    $( "li#box-nlist" ).on("click", "div.tr-nlist",
        function ( e ) {
            var _currentEle = $( this ),
                _ndetailEle = $( "li#box-ndetail" ),
                _fdetailEle = $( "li#box-fdetail" );

            if ( _currentEle.is( "div.tr-nlist" )) {
                var _dtPatternVal = _currentEle.data("dtPattern"),
                    _pattern1Val = _currentEle.data("pattern1"),
                    _pattern2Val = _currentEle.data("pattern2"),
                    _serial = _currentEle.data("serial"),
                    _paramData = $.param({
                        dt_pattern: _dtPatternVal,
                        pattern1: _pattern1Val,
                        pattern2: _pattern2Val,
                        serial: _serial
                    });
                _nutrition.loadTemplate(
                    _url.nutrition.detail, _ndetailEle, _paramData);
                _nutrition.loadTemplate(_url.nutrition.factor.detail,
                    _fdetailEle, _paramData);
            }
        });

    $( "li#box-fdetail" ).on("click", "p#bt-add-fdetail",
        function ( e ) {
            var _currentEle = $( this ),
                _flistEle = $( "li#box-flist" );

            if ( _currentEle.is( "p#bt-add-fdetail" )) {
                _nutrition.loadTemplate(_url.nutrition.factor.list,
                    _flistEle);
            }
        });
});
