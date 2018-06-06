$(document).ready(function () {

    // Import Modules
    var _nutrient = $.taberu.nutrient,
        _url = $.taberu.url,
        _nListEle = $( "div#box-nlist" ),
        _nDetailEle = $( "div#box-ndetail" ),
        _nSubEle = $( "div#box-nsub"),
        _nGetEle = $( "div#box-nget"),
        _fDetailEle = $( "div#box-fdetail" ),
        _fListEle = $( "div#box-flist" );

    // Jquery Custom Events
    // https://learn.jquery.com/events/introduction-to-custom-events/
    _nListEle.on("click", "div.tr",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr" )) {
                var _hasSub = _currentEle.data("hasSub"),
                    _pk = _currentEle.data("nutrientCode"),
                    _param = $.param({ nutrient_code: _pk});
                _nDetailEle.load(_url.api.nutrientForm + "/" + _pk, function () {
                    $("ul#dt_pattern").find("input").prop("disabled", true);
                    $("ul#pattern1").find("input").prop("disabled", true);
                    $("ul#pattern2").find("input").prop("disabled", true);
                });
                _fDetailEle.load(_url.api.factorSet, _param, function () {
                    console.log("Load set of factors complete.");
                });
                if ( _hasSub === "True" ) {
                    _nSubEle.load(_url.api.nutrientSet, _param, function () {
                        console.log("Load set of nutrients complete.");
                    });
                    if ( _nSubEle.is(".off")) {
                        _nSubEle.show();
                        _nSubEle.removeClass("off").addClass("on");
                    }
                } else {
                    if ( _nSubEle.is(".on")) {
                        _nSubEle.removeClass("on").addClass("off");
                        _nSubEle.hide();
                    }
                }
                if ( _fDetailEle.is(".off")) {
                    _fDetailEle.show();
                    _fDetailEle.removeClass("off").addClass("on");
                }
            }
        });

    _nDetailEle.on("click", "ul#dt_pattern > li > input, " +
        "ul#pattern1 > li > input, ul#pattern2 > li > input, li#n-create, " +
        "li#n-update, li#n-reset, li#n-new, li#n-delete",
        function ( e ) {
            var _currentEle = $( this ),
                _nListSectionEle = $( "div#nlist-section" );

            if ( _currentEle.is( "ul#dt_pattern > li > input" ) ) {
                var _dtPattern = _currentEle.val(),
                    _param = $.param({
                        dt_pattern: _dtPattern
                    });
                $( "ul#dt_pattern").find( "input" ).prop("checked", false);
                _currentEle.prop("checked", true);
                $( "ul#pattern1" ).find( "input" ).prop("checked", false);
                $( "ul#pattern2" ).empty();
                _nListSectionEle.load(_url.api.nutrients, _param);

            } else if ( _currentEle.is( "ul#pattern1 > li > input" ) ) {
                var _nPattern2Ele = $("ul#pattern2"),
                    _pattern1 = _currentEle.val(),
                    _param = $.param({
                        dt_pattern: $( "ul#dt_pattern" ).find( "input:checked" )
                            .val(),
                        pattern1: _pattern1
                    });
                $( "ul#pattern1" ).find( "input" ).prop("checked", false);
                _currentEle.prop("checked", true);
                _nListSectionEle.load(_url.api.nutrients, _param);
                _nPattern2Ele.load(_url.api.nutrientPattern2 + "/" + _pattern1);

            } else if ( _currentEle.is( "ul#pattern2 > li > input" ) ) {
                var _dtPattern = $( "ul#dt_pattern" ).find( "input:checked" )
                        .val(),
                    _pattern1 = $( "ul#pattern1" ).find( "input:checked" )
                        .val(),
                    _pattern2 = _currentEle.val(),
                    _param = $.param({
                        dt_pattern: _dtPattern,
                        pattern1: _pattern1,
                        pattern2: _pattern2
                    });
                _nListSectionEle.load(_url.api.nutrients, _param)

            } else if ( _currentEle.is( "li#n-create" ) ) {
                var _form = $( "form#ndetail-form" );
                _form.attr("action", _url.api.nutrients).attr("method", "post")
                    .submit();

            } else if ( _currentEle.is( "li#n-update" ) ) {
                var _nutrientCode = $("div#ndetail-opted-nutrient").data(
                        "nutrientCode"),
                    _json = {
                        has_sub: $("ul#has_sub").find("input:checked")
                            .val(),
                        is_active: $("ul#is_active").find("input:checked")
                            .val(),
                        eng_name: $("input#eng_name").val(),
                        eng_plural: $("input#eng_plural").val(),
                        kor_name: $("input#kor_name").val(),
                        jpn_name: $("input#jpn_name").val(),
                        chn_name: $("input#chn_name").val()
                    };
                $.put(_url.api.nutrients + "/" + _nutrientCode, _json,
                    function () {
                        location.reload();
                    });

            } else if ( _currentEle.is( "li#n-reset" ) ) {
                if ( _currentEle.is( ".new" ) ) {
                    _nDetailEle.load(_url.api.nutrientForm);
                    _nListSectionEle.load(_url.api.nutrients);

                } else if ( _currentEle.is( ".selected" ) ) {
                    var _nutrientCode = $("div#ndetail-opted-nutrient")
                        .data("nutrientCode");
                    _nDetailEle.load(_url.api.nutrientForm + "/" + _nutrientCode,
                        function () {
                            $("ul#dt_pattern").find("input").prop("disabled",
                                true);
                            $("ul#pattern1").find("input").prop("disabled",
                                true);
                            $("ul#pattern2").find("input").prop("disabled",
                                true);
                        })
                }

            } else if ( _currentEle.is( "li#n-new" ) ) {
                _nDetailEle.load(_url.api.nutrientForm);
                _nListSectionEle.load(_url.api.nutrients);
                if ( _nSubEle.is(".on")) {
                    _nSubEle.removeClass("on").addClass("off");
                    _nSubEle.hide();
                }
                if ( _nGetEle.is(".on")) {
                    _nGetEle.removeClass("on").addClass("off");
                    _nGetEle.hide();
                }
                if ( _fDetailEle.is(".on") ) {
                    _fDetailEle.removeClass("on").addClass("off");
                    _fDetailEle.hide();
                }
                if ( _fListEle.is(".on") ) {
                    _fListEle.removeClass("on").addClass("off");
                    _fListEle.hide();
                }

            } else if ( _currentEle.is( "li#n-delete" ) ) {
                var _nutrientCode = $("div#ndetail-opted-nutrient")
                        .data("nutrientCode");
                $.delete(_url.api.nutrients + "/" + _nutrientCode, function () {
                    location.reload();
                });

            }
        });

    _nSubEle.on("click", "li#nsub-get",
        function ( e ) {
            var _currentEle = $( this ),
                _nGetSectionEle = $( "div#nget-section" ),
                _nGetOptionEle = $("div#nget-option");

            if ( _currentEle.is( "li#nsub-get" ) ) {
                _nGetSectionEle.load(_url.api.nutrients);
                _nGetOptionEle.load(_url.api.nutrientOption);
                if ( _nGetEle.is(".off")) {
                    _nGetEle.show();
                    _nGetEle.removeClass("off").addClass("on");
                }
            }
        });
    
    _nGetEle.on("click, change", "select#dt_pattern, select#pattern1, " +
        "select#pattern2",
        function ( e ) {
            var _currentEle = $( this );
            
            if ( _currentEle.is("select#dt_pattern") ) {
                console.log("select dt_pattern");
            } else if ( _currentEle.is("select#pattern1" ) ) {
                var _pattern1Val = _currentEle.val();
                $.get(_url.api.nutrientOption + "/" + _pattern1Val,
                    function ( data ) {
                        $("select#pattern2").parent().replaceWith(data);
                    });
            } else if ( _currentEle.is("select#pattern2" ) ) {
                console.log("select pattern2");
            }
        });

    _fDetailEle.on("click", "div.tr, li#get-flist, li#delete-flist, " +
        "li#update-flist",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr" ) ) {
                var _optedEle = _fDetailEle.find( "div.opted-factor" ),
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
                _optedEle.load(_url.api.factorSet + "/" + _pk);

                if ( _wrapBt.is(".off") ) {
                    $( "li#delete-flist" ).show();
                    $( "li#update-flist" ).show();
                    _wrapBt.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is( "li#get-flist" ) ) {
                _fListEle.load(_url.api.factors);
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
                $.delete(_url.api.factorSet + "/" + _pk, function ( data ) {
                    _fDetailEle.load(_url.api.factorSet + "/" + _nutrientCode);
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
                $.put(_url.api.factorSet + "/" + _pk, function ( data ) {
                    _fDetailEle.load(_url.api.factorSet + "/" + _nutrientCode);
                });

            }
        });

    _fListEle.on("click", "div.tr, li#flist-reset, li#flist-add",
        function ( e ) {
            var _currentEle = $( this );

            if( _currentEle.is( "div.tr" ) ) {
                var _pk = _currentEle.data("code"),
                    _json = $.param({factor_code: _pk});
                _nutrient.toggleTableOfRows(_url.api.factors, _json,
                    _currentEle);
                if ( _currentEle.is(".sub") ) {
                    var _optedEle = _fListEle.find( "div.opted-factor" ),
                        _addEle = $( "li#flist-add" );
                    _optedEle.load(_url.api.factors + "/" + _pk);
                    if (_addEle.is(".off")) {
                        _addEle.show().removeClass("off").addClass("on");
                    }
                }

            } else if ( _currentEle.is( "li#flist-reset" ) ) {
                $( "li#get-flist" ).trigger("click");

            } else if ( _currentEle.is( "li#flist-add" ) ) {
                var _optedFactor = $( "div#box-flist" ).find( "div.opted-factor" ),
                    _optedNutrient = $( "div#opted-nutrient" ),
                    _selectedUnit = _fListEle.find("select#unit > option:checked" ),
                    _inputVal = _fListEle.find( "input#quantity" ).val(),
                    _json = {
                        factor_code: _optedFactor.data("factorCode"),
                        nutrient_code: _optedNutrient.data("nutrientCode"),
                        unit_code: _selectedUnit.data("unitCode"),
                        quantity: _inputVal
                    };
                $.post( _url.api.factorSet, _json, function ( data ) {
                    var _fDetailEle = $( "div#box-fdetail" ),
                        _pk = $( "div#opted-nutrient" ).data("nutrientCode");
                    _fDetailEle.load(_url.api.factorSet + "/" + _pk);
                    $( "div#message-flist" ).text(data);
                });

            }
        });

});
