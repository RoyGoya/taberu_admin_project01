$(document).ready(function () {

    // Module Pattern
    // https://learn.jquery.com/code-organization/concepts/
    var _nutrient = $.taberu.nutrient,
        _url = $.taberu.url;

    // Jquery Custom Events
    // https://learn.jquery.com/events/introduction-to-custom-events/
    $( "div#box-nlist" ).on("click", "div.tr-nlist",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr-nlist" )) {
                var _nDetailEle = $( "div#box-ndetail" ),
                    _fDetailEle = $( "div#box-fdetail" ),
                    _pk = _currentEle.data("nutrientCode");
                _nutrient.loadTemplate(_url.api.nutrientForm + "/" + _pk,
                    _nDetailEle);
                _nutrient.loadTemplate(_url.api.factorSet + "/" + _pk,
                    _fDetailEle);
                if ( _fDetailEle.is(".off")) {
                    _fDetailEle.show();
                    _fDetailEle.removeClass("off").addClass("on");
                }
            }
        });

    $( "div#box-ndetail" ).on("click", "ul#dt_pattern > li > input, " +
        "ul#pattern1 > li > input, ul#pattern2 > li > input, li#n-send, " +
        "li#n-reset, li#n-new",
        function ( e) {
            var _currentEle = $( this );

            if ( _currentEle.is( "ul#dt_pattern > li > input" ) ) {
                var _nListEle = $( "div#box-nlist" ),
                    _json = { dt_pattern: _currentEle.val() };
                _nutrient.clearCheckedInputs($( "ul#dt_pattern")
                    .find( "input" ));
                _currentEle.prop("checked", true);
                _nutrient.clearCheckedInputs($( "ul#pattern1" )
                    .find( "input" ));
                $( "ul#pattern2" ).empty();
                _nutrient.loadTemplate(_url.api.nutrients, _nListEle, _json);

            } else if ( _currentEle.is( "ul#pattern1 > li > input" ) ) {
                var _nListEle = $( "div#box-nlist" ),
                    _nPattern2Ele = $("ul#pattern2").empty(),
                    _pattern1Inputs = $( "ul#pattern1" ).find( "input" ),
                    _pattern1Vla = _currentEle.val(),
                    _json = {
                        dt_pattern: $( "ul#dt_pattern" ).find( "input:checked" )
                            .val(),
                        pattern1: _pattern1Vla};
                _nutrient.clearCheckedInputs(_pattern1Inputs);
                _currentEle.prop("checked", true);
                _nutrient.loadTemplate(_url.api.nutrients, _nListEle, _json);
                _nutrient.loadTemplate(_url.api.nutrientPattern2, _nPattern2Ele,
                    { pattern1: _pattern1Vla });

            } else if ( _currentEle.is( "ul#pattern2 > li > input" ) ) {
                console.log("pattern2");

            } else if ( _currentEle.is( "li#n-send" ) ) {
                console.log("n-send");

            } else if ( _currentEle.is( "li#n-reset" ) ) {
                var _nDetailEle = $( "div#box-ndetail" ),
                    _nListEle = $( "div#box-nlist" );
                if ( _currentEle.is( ".new" ) ) {
                    _nutrient.loadTemplate(_url.api.nutrientForm, _nDetailEle);
                    _nutrient.loadTemplate(_url.api.nutrients, _nListEle,
                        { dt_pattern: 's'});
                } else if ( _currentEle.is( ".selected" ) ) {
                    var _selectedItemEle = $( "div#selected-nutrients" ),
                        _json = {
                            dt_pattern: _selectedItemEle.data("dtPattern"),
                            pattern1: _selectedItemEle.data("pattern1"),
                            pattern2: _selectedItemEle.data("pattern2"),
                            serial: _selectedItemEle.data("serial")
                        };
                    _nutrient.loadTemplate(_url.api.nutrients, _nDetailEle,
                        _json);
                }

            } else if ( _currentEle.is( "li#n-new" ) ) {
                var _nDetailEle = $( "div#box-ndetail" ),
                    _fDetailEle = $( "div#box-fdetail" ),
                    _fListEle = $( "div#box-flist" );
                _nutrient.loadTemplate(_url.api.nutrients, _nDetailEle);
                if ( _fDetailEle.is(".on") ) {
                    _fDetailEle.removeClass("on").addClass("off");
                    _fDetailEle.hide();
                }
                if ( _fListEle.is(".on") ) {
                    _fListEle.removeClass("on").addClass("off");
                    _fListEle.hide();
                }
            }
        });

    $( "div#box-fdetail" ).on("click", "div.tr-fdetail, li#get-flist",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr-fdetail" ) ) {
                var _markedEle = $( "div#box-fdetail" ).find( "div.opted-factor" ).empty(),
                    _wrapBt = $( "ul#fdtail-wrap-bt" ),
                    _pk = _currentEle.data("factorCode");
                _currentEle.prevAll(".opted").removeClass("opted")
                    .css("background-color", "white");
                _currentEle.nextAll(".opted").removeClass("opted")
                    .css("background-color", "white");
                if (_currentEle.not(".opted")) {
                    _currentEle.addClass( "opted" );
                    _currentEle.css( "background-color", "beige" );
                }
                _nutrient.replaceTemplate(_url.api.factors + "/" + _pk,
                       _markedEle);

                if ( _wrapBt.is(".off") ) {
                    var _btDelete = $( "<li class='bt'>" ).text("DELETE"),
                        _btUpdate = $( "<li class='bt'>" ).text("UPDATE");
                    _wrapBt.append(_btDelete).append(_btUpdate);
                    _wrapBt.removeClass("off").addClass("on")
                }
            } else if ( _currentEle.is( "li#get-flist" )) {
                var _fListEle = $( "div#box-flist" );
                _nutrient.loadTemplate(_url.api.factors, _fListEle);
                if ( _fListEle.is(".off") ) {
                    _fListEle.show();
                    _fListEle.removeClass("off").addClass("on");
                }
            }
        });

    $( "div#box-flist" ).on("click", "div.tr-flist, li#flist-reset," +
        "li#flist-add",
        function ( e ) {
           var _currentEle = $( this );

           if( _currentEle.is( "div.tr-flist" ) ) {
               var _pk = _currentEle.data("code");
               _nutrient.toggleTableOfRows(_url.api.factorList + "/" + _pk,
                   _currentEle);
               if ( _currentEle.is(".sub") ) {
                   var _markedEle = $( "div#box-flist" ).find( "div.opted-factor" ).empty(),
                       _addEle = $( "li#flist-add" );
                   _nutrient.replaceTemplate(_url.api.factors + "/" + _pk,
                       _markedEle);
                   if (_addEle.is(".off")) {
                       _addEle.show().removeClass("off").addClass("on");
                   }
               }
           } else if ( _currentEle.is( "li#flist-reset" ) ) {
                var _flistEle = $( "div#box-flist" ),
                    _addEle = $( "li#flist-add" );
                _nutrient.loadTemplate(_url.factorList, _flistEle, { type: 'initial' });
                if (_addEle.is(".on")) {
                    _addEle.hide().removeClass("on").addClass("off");
                }
           } else if ( _currentEle.is( "li#flist-add" ) ) {
                var _optedFactor = $( "div#opted-factor" ),
                    _optedNutrient = $( "div#opted-nutrient" ),
                    _selectedUnit = $( "select#factor-unit > option:checked" ),
                    _inputVal = $( "input#selected-txt" ).val(),
                    _json = {
                        factor_code: _optedFactor.data("factorCode"),
                        nutrient_code: _optedNutrient.data("nutrientCode"),
                        unit_code: _selectedUnit.data("unitCode"),
                        quantity: _inputVal
                    },
                    _doneFunc = function () {
                        var _fDetailEle = $( "div#box-fdetail" ),
                            _pk = _optedNutrient.data("nutrientCode");
                        _nutrient.loadTemplate(_url.api.factorSet + "/" + _pk,
                            _fDetailEle);
                    };
                _nutrient.postSetOfAFactor(_url.api.factorSet, _json, _doneFunc);
           }
        });

});
