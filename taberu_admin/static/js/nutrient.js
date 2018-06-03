$(document).ready(function () {

    // Import Modules
    var _nutrient = $.taberu.nutrient,
        _url = $.taberu.url,
        _nListEle = $( "div#box-nlist" ),
        _nDetailEle = $( "div#box-ndetail" ),
        _fDetailEle = $( "div#box-fdetail" ),
        _fListEle = $( "div#box-flist" );

    // Jquery Custom Events
    // https://learn.jquery.com/events/introduction-to-custom-events/
    _nListEle.on("click", "div.tr-nlist",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr-nlist" )) {
                var _pk = _currentEle.data("nutrientCode");
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

    _nDetailEle.on("click", "ul#dt_pattern > li > input, " +
        "ul#pattern1 > li > input, ul#pattern2 > li > input, li#n-create, " +
        "li#n-update, li#n-reset, li#n-new",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "ul#dt_pattern > li > input" ) ) {
                var _dtPattern = _currentEle.val();
                _nutrient.clearCheckedInputs($( "ul#dt_pattern")
                    .find( "input" ));
                _currentEle.prop("checked", true);
                _nutrient.clearCheckedInputs($( "ul#pattern1" ).find( "input" ));
                $( "ul#pattern2" ).empty();
                _nutrient.loadTemplate(_url.api.nutrients + "/" + _dtPattern,
                    _nListEle);

            } else if ( _currentEle.is( "ul#pattern1 > li > input" ) ) {
                var _nPattern2Ele = $("ul#pattern2"),
                    _pattern1Inputs = $( "ul#pattern1" ).find( "input" ),
                    _dtPattern = $( "ul#dt_pattern" ).find( "input:checked" ).val(),
                    _pattern1 = _currentEle.val();
                _nutrient.clearCheckedInputs(_pattern1Inputs);
                _currentEle.prop("checked", true);
                _nutrient.loadTemplate(_url.api.nutrients + "/" + _dtPattern
                    + "-" + _pattern1, _nListEle);
                _nutrient.loadTemplate(_url.api.nutrientPattern2 + "/"
                    + _pattern1, _nPattern2Ele);

            } else if ( _currentEle.is( "ul#pattern2 > li > input" ) ) {
                var _dtPattern = $( "ul#dt_pattern" ).find( "input:checked" ).val(),
                    _pattern1 = $( "ul#pattern1" ).find( "input:checked" ).val(),
                    _pattern2 = _currentEle.val(),
                    _pk = _dtPattern + "-" + _pattern1 + "-" + _pattern2;
                _nutrient.loadTemplate(_url.api.nutrients + "/" + _pk,
                    _nListEle);

            } else if ( _currentEle.is( "li#n-create" ) ) {
                console.log("n-create");

            } else if ( _currentEle.is( "li#n-update" ) ) {
                console.log("n-update");

            } else if ( _currentEle.is( "li#n-reset" ) ) {
                var _dtPattern = "s";
                if ( _currentEle.is( ".new" ) ) {
                    _nutrient.loadTemplate(_url.api.nutrientForm, _nDetailEle);
                    _nutrient.loadTemplate(_url.api.nutrients + "/" + _dtPattern,
                        _nListEle);
                } else if ( _currentEle.is( ".selected" ) ) {
                    var _nutrientCode = $("div#ndetail-opted-nutrient")
                        .data("nutrientCode");
                    _nutrient.loadTemplate(_url.api.nutrientForm + "/"
                        + _nutrientCode, _nDetailEle);
                }

            } else if ( _currentEle.is( "li#n-new" ) ) {
                _nutrient.loadTemplate(_url.api.nutrientForm, _nDetailEle);
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

    _fDetailEle.on("click", "div.tr-fdetail, li#get-flist, " +
        "li#delete-flist, li#update-flist",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr-fdetail" ) ) {
                var _markedEle = _fDetailEle.find( "div.opted-factor" ),
                    _wrapBt = $( "ul#fdtail-wrap-bt" ),
                    _pk = $("div#opted-nutrient").data("nutrientCode") + "-" +
                        _currentEle.data("factorCode");
                _currentEle.prevAll(".opted").removeClass("opted")
                    .css("background-color", "white");
                _currentEle.nextAll(".opted").removeClass("opted")
                    .css("background-color", "white");
                if (_currentEle.not(".opted")) {
                    _currentEle.addClass( "opted" );
                    _currentEle.css( "background-color", "beige" );
                }
                _nutrient.replaceTemplate(_url.api.factorSet + "/" + _pk,
                       _markedEle);
                if ( _wrapBt.is(".off") ) {
                    $( "li#delete-flist" ).show();
                    $( "li#update-flist" ).show();
                    _wrapBt.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is( "li#get-flist" ) ) {
                var _fListEle = $( "div#box-flist" );
                _nutrient.loadTemplate(_url.api.factors, _fListEle);
                if ( _fListEle.is(".off") ) {
                    _fListEle.show();
                    _fListEle.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is( "li#delete-flist" ) ) {
                var _nutrientCode = $( "div#opted-nutrient" ).data(
                    "nutrientCode"),
                    _factorCode = _fDetailEle.find( "div.opted-factor" )
                        .data("factorCode"),
                    _pk = _nutrientCode + "-" + _factorCode;
                $.delete(_url.api.factorSet + "/" + _pk, function () {
                    _nutrient.loadTemplate(_url.api.factorSet + "/"
                        + _nutrientCode, _fDetailEle);
                });

            } else if ( _currentEle.is( "li#update-flist" ) ) {
                var _nutrientCode = $( "div#opted-nutrient" ).data(
                    "nutrientCode"),
                    _factorCode = _fDetailEle.find( "div.opted-factor" ).data(
                        "factorCode"),
                    _selectedUnit = _fDetailEle.find(
                        "select#unit > option:checked" ).val(),
                    _inputVal = _fDetailEle.find( "input#quantity" ).val(),
                    _pk = _nutrientCode + "-" + _factorCode + "-"
                        + _selectedUnit + "-" + _inputVal;
                $.put(_url.api.factorSet + "/" + _pk, function () {
                    _nutrient.loadTemplate(_url.api.factorSet + "/"
                        + _nutrientCode, _fDetailEle);
                });

            }
        });

    _fListEle.on("click", "div.tr-flist, li#flist-reset," +
        "li#flist-add",
        function ( e ) {
           var _currentEle = $( this );

           if( _currentEle.is( "div.tr-flist" ) ) {
               var _pk = _currentEle.data("code");
               _nutrient.toggleTableOfRows(_url.api.factorList + "/" + _pk,
                   _currentEle);
               if ( _currentEle.is(".sub") ) {
                   var _markedEle = _fListEle.find( "div.opted-factor" ),
                       _addEle = $( "li#flist-add" );
                   _nutrient.replaceTemplate(_url.api.factors + "/" + _pk,
                       _markedEle);
                   if (_addEle.is(".off")) {
                       _addEle.show().removeClass("off").addClass("on");
                   }
               }

           } else if ( _currentEle.is( "li#flist-reset" ) ) {
                $( "li#get-flist" ).trigger("click");

           } else if ( _currentEle.is( "li#flist-add" ) ) {
                var _optedFactor = $( "div#box-flist" ).find( "div.opted-factor" ),
                    _optedNutrient = $( "div#opted-nutrient" ),
                    _selectedUnit = $( "select#factor-unit > option:checked" ),
                    _inputVal = $( "input#factor-quantity" ).val(),
                    _json = {
                        factor_code: _optedFactor.data("factorCode"),
                        nutrient_code: _optedNutrient.data("nutrientCode"),
                        unit_code: _selectedUnit.data("unitCode"),
                        quantity: _inputVal
                    };
                _nutrient.postSetOfAFactor(_url.api.factorSet, _json);

           }
        });

});
