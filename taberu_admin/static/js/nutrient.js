$(document).ready(function () {

    // Module Pattern
    // https://learn.jquery.com/code-organization/concepts/
    var _nutrient = $.taberu.nutrient,
        _url = $.taberu.url;

    // Jquery Custom Events
    // https://learn.jquery.com/events/introduction-to-custom-events/
    $( "div#box-nlist" ).on("click", "div.tr-nlist",
        function ( e ) {
            var _currentEle = $( this ),
                _ndetailEle = $( "div#box-ndetail" ),
                _fdetailEle = $( "div#box-fdetail" );

            if ( _currentEle.is( "div.tr-nlist" )) {
                var _paramData = $.param({
                        dt_pattern: _currentEle.data("dtPattern"),
                        pattern1: _currentEle.data("pattern1"),
                        pattern2: _currentEle.data("pattern2"),
                        serial: _currentEle.data("serial")
                    });
                _nutrient.loadTemplate(_url.nutrient.detail, _ndetailEle,
                    _paramData);
                _nutrient.loadTemplate(_url.factor.detail, _fdetailEle,
                    _paramData);
                if ( _fdetailEle.is(".off")) {
                    _fdetailEle.show();
                    _fdetailEle.removeClass("off").addClass("on");
                }
            }
        });

    $( "div#box-ndetail" ).on("click", "ul#dt_pattern > li > input, " +
        "ul#pattern1 > li > input, ul#pattern2 > li > input, li#n-send, " +
        "li#n-reset, li#n-new",
        function ( e) {
            var _currentEle = $( this ),
                _ndetailEle = $( "div#box-ndetail" ),
                _fdetailEle = $( "div#box-fdetail" ),
                _flistEle = $( "div#box-flist" ),
                _dtPatternEle = $( "ul#dt_pattern" ),
                _pattern1Ele = $( "ul#pattern1" ),
                _pattern2Ele = $( "ul#pattern2" ),
                _nlistEle = $( "div#box-nlist" );

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

            } else if ( _currentEle.is( "li#n-send" ) ) {
                console.log("n-send");
            } else if ( _currentEle.is( "li#n-reset" ) ) {
                if ( _currentEle.is( ".new" ) ) {
                    _nutrient.loadTemplate(_url.nutrient.detail,
                        _ndetailEle);
                } else if ( _currentEle.is( ".selected" ) ) {
                    var _selectedItemEle = $( "div#selected-nutrient" ),
                        _paramData = $.param({
                            dt_pattern: _selectedItemEle.data("dtPattern"),
                            pattern1: _selectedItemEle.data("pattern1"),
                            pattern2: _selectedItemEle.data("pattern2"),
                            serial: _selectedItemEle.data("serial")
                        });
                    _nutrient.loadTemplate(_url.nutrient.detail,
                        _ndetailEle, _paramData);
                }
            } else if ( _currentEle.is( "li#n-new" ) ) {
                _nutrient.loadTemplate(_url.nutrient.detail,
                        _ndetailEle);
                if ( _fdetailEle.is(".on") ) {
                    _fdetailEle.removeClass("on").addClass("off");
                    _fdetailEle.hide();
                }
                if ( _flistEle.is(".on") ) {
                    _flistEle.removeClass("on").addClass("off");
                    _flistEle.hide();
                }
            }
        });

    $( "div#box-fdetail" ).on("click", "li#get-flist",
        function ( e ) {
            var _currentEle = $( this ),
                _flistEle = $( "div#box-flist" );

            if ( _currentEle.is( "li#get-flist" )) {
                var _paramData = $.param({
                    type: 'initial'
                });
                _nutrient.loadTemplate(_url.factor.list,
                    _flistEle, _paramData);
                if ( _flistEle.is(".off") ) {
                    _flistEle.show();
                    _flistEle.removeClass("off").addClass("on");
                }
            }
        });

    $( "div#box-flist" ).on("click", "div.tr-flist, li#bt-reset",
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
                   var _markedEle = $( "div#selected-factor" ).empty(),
                       _wrapBtEle = $( "ul#flist-wrap-bt" ),
                       _liBt = $( "<li>" ).addClass("bt bt-add");
                   _nutrient.replaceTemplate(_url.factor.select, _markedEle,
                       _paramData);
                   if (_wrapBtEle.is(".off")) {
                       _wrapBtEle.append(_liBt.text("ADD"));
                       _wrapBtEle.removeClass("off");
                       _wrapBtEle.addClass("on");
                   }
               }
           } else if ( _currentEle.is("li#bt-reset")) {
                var _flistEle = $( "div#box-flist" ),
                    _wrapBtEle = $( "ul#flist-wrap-bt" ),
                    _paramData = $.param({
                        type: 'initial'
                    });
                _nutrient.loadTemplate(_url.factor.list,
                    _flistEle, _paramData);
                if (_wrapBtEle.is(".on")) {
                    _wrapBtEle.find(".bt-add").remove();
                    _wrapBtEle.removeClass("on");
                    _wrapBtEle.addClass("off");
                }
           }

        });
});
