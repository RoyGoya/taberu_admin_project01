$(document).ready(function () {

    // Module Pattern
    // https://learn.jquery.com/code-organization/concepts/
    var _nutrient = $.taberu.nutrient,
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
                var _paramData = $.param({ dt_pattern: _currentEle.val()});
                _nutrient.clearCheckedInputEls(
                    $( "ul#dt_pattern").find( "input" ));
                _currentEle.prop("checked", true);
                _nutrient.clearCheckedInputEls(
                    $( "ul#pattern1" ).find( "input" ));
                _pattern2Ele.empty();
                _nutrient.loadTemplate(_url.nutrient.list, _nlistEle,
                    _paramData);

            } else if ( _currentEle.is( "ul#pattern1 > li > input" ) ) {
                var _pattern1Inputs = _pattern1Ele.find( "input" ),
                    _pattern1Vla = _currentEle.val(),
                    _paramData = $.param({
                        dt_pattern: _dtPatternEle.find( "input:checked" )
                            .val(),
                        pattern1: _pattern1Vla
                    });
                _nutrient.clearCheckedInputEls(_pattern1Inputs);
                _currentEle.prop("checked", true);
                _nutrient.loadTemplate(_url.nutrient.list, _nlistEle,
                    _paramData);
                _nutrient.getNutrientPattern2(_url.nutrient.pattern2,
                    _pattern1Vla);

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
                var _paramData = $.param({
                        dt_pattern: _currentEle.data("dtPattern"),
                        pattern1: _currentEle.data("pattern1"),
                        pattern2: _currentEle.data("pattern2"),
                        serial: _currentEle.data("serial")
                    });
                _nutrient.loadTemplate(_url.nutrient.detail,
                    _ndetailEle, _paramData);
                _nutrient.loadTemplate(_url.nutrient.factor.detail,
                    _fdetailEle, _paramData);
            }
        });

    $( "li#box-fdetail" ).on("click", "p#bt-get-flist",
        function ( e ) {
            var _currentEle = $( this ),
                _flistEle = $( "li#box-flist" );

            if ( _currentEle.is( "p#bt-get-flist" )) {
                var _paramData = $.param({
                    type: 'initial'
                });
                _nutrient.loadTemplate(_url.nutrient.factor.list,
                    _flistEle, _paramData);
            }
        });

    $( "li#box-flist" ).on("click", "div.tr-flist, li#bt-reset",
        function ( e ) {
           var _currentEle = $( this );

           if( _currentEle.is("div.tr-flist") ) {
               var _paramData = $.param({
                   type: 'addition',
                   pattern1: _currentEle.data("pattern1"),
                   pattern2: _currentEle.data("pattern2"),
                   pattern3: _currentEle.data("pattern3"),
                   pattern4: _currentEle.data("pattern4")
               });
               _nutrient.toggleListOfEls(_currentEle, _paramData);
               if ( _currentEle.is(".sub") ) {
                   var _markedEle = $( "ul#selected-factor" ).empty(),
                       _wrapBtEle = $( "ul#wrap-bt" ),
                       _liBt = $( "<li>" ).addClass("bt bt-add"),
                       _vals = [_currentEle.data("code"),
                                _currentEle.data("engName"),
                                _currentEle.data("korName")];
                   _vals.forEach(function (val, idx) {
                       var _li = $('<li>').text(val);
                       _markedEle.append( _li );
                   });
                   // TODO: Add Selected Factor.
                   _markedEle.append($("<select>")
                       .append($("<option>").attr("value", "test")
                           .text("test")));
                   _markedEle.append($("<input>").attr("type", "text"));
                   if (_wrapBtEle.is(".off")) {
                       _wrapBtEle.append(_liBt.text("ADD"));
                       _wrapBtEle.removeClass("off");
                       _wrapBtEle.addClass("on");
                   }

               }
           } else if ( _currentEle.is("li#bt-reset")) {
                var _flistEle = $( "li#box-flist" ),
                    _wrapBtEle = $( "ul#wrap-bt" ),
                    _paramData = $.param({
                        type: 'initial'
                    });
                _nutrient.loadTemplate(_url.nutrient.factor.list,
                    _flistEle, _paramData);
                if (_wrapBtEle.is(".on")) {
                    _wrapBtEle.find(".bt-add").remove();
                    _wrapBtEle.removeClass("on");
                    _wrapBtEle.addClass("off");
                }
           }

        });
});
