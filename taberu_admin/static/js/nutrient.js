$(document).ready(function () {

    // Import Modules
    // Encapsulated Functions
    // Abstracted Urls
    // Partitioned Element Delegations.
    var _nutrient = $.taberu.nutrient,
        _url = $.taberu.url,
        _nListEle = $( "div#box-nlist" ),
        _nDetailEle = $( "div#box-ndetail" ),
        _nSubEle = $( "div#box-nsub"),
        _nGetEle = $( "div#box-nget"),
        _fDetailEle = $( "div#box-fdetail" ),
        _fListEle = $( "div#box-flist" );

    // Using Event Delegation
    // For prevent event propagation
    // And anchoring asynchronous loaded documents.
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
                    if ( _nSubEle.is(".off") ) {
                        _nSubEle.show();
                        _nSubEle.removeClass("off").addClass("on");
                    }
                } else {
                    if ( _nSubEle.is(".on") ) {
                        _nSubEle.removeClass("on").addClass("off");
                        _nSubEle.hide();
                    }
                    if ( _nGetEle.is(".on") ) {
                        _nGetEle.removeClass("on").addClass("off");
                        _nGetEle.hide();
                    }
                }
                if ( _fDetailEle.is(".off") ) {
                    _fDetailEle.show();
                    _fDetailEle.removeClass("off").addClass("on");
                }
                if ( _fListEle.is(".on") ) {
                    _fListEle.removeClass("on").addClass("off");
                    _fListEle.hide();
                }
            }
        });

    _nDetailEle.on("click", "ul#dt_pattern > li > input, " +
        "ul#pattern1 > li > input, ul#pattern2 > li > input, li.bt-create, " +
        "li.bt-update, li.bt-reset, li.bt-new, li.bt-delete",
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

            } else if ( _currentEle.is( "li.bt-create" ) ) {
                var _form = $( "form#ndetail-form" );
                _form.attr("action", _url.api.nutrients).attr("method", "post")
                    .submit();

            } else if ( _currentEle.is( "li.bt-update" ) ) {
                var _nutrientCode = _nDetailEle.find("div.delegate-item").data(
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

            } else if ( _currentEle.is( "li.bt-reset" ) ) {
                if ( _currentEle.is( ".new" ) ) {
                    _nDetailEle.load(_url.api.nutrientForm);
                    _nListSectionEle.load(_url.api.nutrients);

                } else if ( _currentEle.is( ".selected" ) ) {
                    var _nutrientCode = _nDetailEle.find("div.delegate-item").data(
                        "nutrientCode");
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

            } else if ( _currentEle.is( "li.bt-new" ) ) {
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

            } else if ( _currentEle.is( "li.bt-delete" ) ) {
                var _nutrientCode = _nDetailEle.find("div.delegate-item").data(
                        "nutrientCode");
                $.delete(_url.api.nutrients + "/" + _nutrientCode, function () {
                    location.reload();
                });

            }
        });

    _nSubEle.on("click", "div.tr, li.bt-get, li.bt-delete, li.bt-update",
        function ( e ) {
            var _currentEle = $( this ),
                _nGetSectionEle = _nGetEle.find( "div.tb-section" ),
                _nGetOptionEle = _nGetEle.find( "div.option" );

            if ( _currentEle.is( "div.tr" ) ) {
                var _deleteBt = _nSubEle.find("li.bt-delete"),
                    _updateBt = _nSubEle.find("li.bt-update");
                if ( _deleteBt.is(".off") ) {
                    _deleteBt.show();
                    _deleteBt.removeClass("off").addClass("on");
                }
                if ( _updateBt.is(".off") ) {
                    _updateBt.show();
                    _updateBt.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is( "li.bt-get" ) ) {
                _nGetSectionEle.load(_url.api.nutrients);
                _nGetOptionEle.load(_url.api.nutrientOption);
                if ( _nGetEle.is(".off")) {
                    _nGetEle.show();
                    _nGetEle.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is( "li.bt-delete" ) ) {

            } else if ( _currentEle.is( "li.bt-update" ) ) {

            }
        });
    
    _nGetEle.on("change", "select#dt_pattern, select#pattern1, select#pattern2",
        function ( e ) {
            var _currentEle = $( this ),
                _nGetSectionEle = _nGetEle.find( "div.tb-section" );
            
            if ( _currentEle.is( "select#dt_pattern" ) ) {
                var _param = $.param({dt_pattern: _currentEle.val()});
                _nGetSectionEle.load(_url.api.nutrients, _param);
                $( "select#pattern1 > option:selected" ).prop("selected", false);
                $( "select#pattern2 > option:selected" ).prop("selected", false);

            } else if ( _currentEle.is( "select#pattern1" ) ) {
                if (_currentEle.val() === 'empty') {
                    return false
                }
                var _pattern1 = _currentEle.val(),
                    _dtPattern = $("select#dt_pattern > option:selected").val()
                    _param = $.param({
                        dt_pattern: _dtPattern,
                        pattern1: _pattern1
                    });
                $.get(_url.api.nutrientOption + "/" + _pattern1,
                    function ( data ) {
                        $("select#pattern2").parent().replaceWith(data);
                    });
                _nGetSectionEle.load(_url.api.nutrients, _param);

            } else if ( _currentEle.is( "select#pattern2" ) ) {
                if (_currentEle.val() === 'empty') {
                    return false
                }
                var _dtPattern = $("select#dt_pattern > option:selected").val(),
                    _pattern1 = $("select#pattern1 > option:selected").val(),
                    _pattern2 = _currentEle.val(),
                    _param = $.param({
                        dt_pattern: _dtPattern,
                        pattern1: _pattern1,
                        pattern2: _pattern2
                    });
                _nGetSectionEle.load(_url.api.nutrients, _param);

            }
        });
    
    _nGetEle.on("click", "div.tr, li.bt-reset, li.bt-add",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr" ) ) {
                var _nutrientCode = _currentEle.data("nutrientCode"),
                    _optedSectionEle = _nGetEle.find("div.opted-item"),
                    _addBt = _nGetEle.find("li.bt-add");
                _optedSectionEle.load(_url.api.nutrients + "/" + _nutrientCode);
                if ( _addBt.is(".off") ) {
                    _addBt.show();
                    _addBt.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is("li.bt-reset") ) {
                var _addBt = _nGetEle.find("li.bt-add");
                _nSubEle.find("li.bt-get").trigger("click");
                _nGetEle.find("div.opted-item").empty();
                if ( _addBt.is(".on") ) {
                    _addBt.hide();
                    _addBt.removeClass("on").addClass("off");
                }

            } else if ( _currentEle.is("li.bt-add") ) {
                var _nutrientCode = _nSubEle.find("div.delegate-item").data("nutrientCode"),
                    _optedItemCode = _nGetEle.find("form").data("nutrientCode"),
                    _unitCode = _nGetEle.find("select#unit > option:selected").val(),
                    _quantity = _nGetEle.find("input#quantity").val(),
                    _json = {
                        super_code: _nutrientCode,
                        sub_code: _optedItemCode,
                        unit_code: _unitCode,
                        quantity: _quantity
                    };
                $.post(_url.api.nutrientSet, _json, function () {
                    _nSubEle.load(_url.api.nutrientSet,
                        $.param({nutrient_code: _nutrientCode}));
                });

            }

        });

    _fDetailEle.on("click", "div.tr, li.bt-get, li.bt-delete, li.bt-update",
        function ( e ) {
            var _currentEle = $( this );

            if ( _currentEle.is( "div.tr" ) ) {
                var _optedEle = _fDetailEle.find( "div.opted-item" ),
                    _wrapBt = _fDetailEle.find("div.wrap-bt"),
                    _nutrientCode = _fDetailEle.find("div.delegate-item")
                        .data("nutrientCode"),
                    _factorCode = _currentEle.data("factorCode"),
                    _pk = _nutrientCode + "-" + _factorCode;
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
                    _fDetailEle.find( "li.bt-delete" ).show();
                    _fDetailEle.find( "li.bt-update" ).show();
                    _wrapBt.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is( "li.bt-get" ) ) {
                _fListEle.load(_url.api.factors);
                if ( _fListEle.is(".off") ) {
                    _fListEle.show();
                    _fListEle.removeClass("off").addClass("on");
                }

            } else if ( _currentEle.is( "li.bt-delete" ) ) {
                var _nutrientCode = _fDetailEle.find("div.delegate-item")
                        .data("nutrientCode"),
                    _factorCode = _fDetailEle.find( "div.opted-item" )
                        .data("factorCode"),
                    _pk = _nutrientCode + "-" + _factorCode;
                $.delete(_url.api.factorSet + "/" + _pk, function ( data ) {
                    _fDetailEle.load(_url.api.factorSet + "/" + _nutrientCode);
                });

            } else if ( _currentEle.is( "li.bt-update" ) ) {
                var _nutrientCode = _fDetailEle.find("div.delegate-item")
                        .data("nutrientCode"),
                    _factorCode = _fDetailEle.find( "div.opted-item" ).data(
                        "factorCode"),
                    _selectedUnit = _fDetailEle.find(
                        "select.unit > option:checked" ).val(),
                    _inputVal = _fDetailEle.find( "input#quantity" ).val(),
                    _pk = _nutrientCode + "-" + _factorCode + "-"
                        + _selectedUnit + "-" + _inputVal;
                $.put(_url.api.factorSet + "/" + _pk, function ( data ) {
                    _fDetailEle.load(_url.api.factorSet + "/" + _nutrientCode);
                });

            }
        });

    _fListEle.on("click", "div.tr, li.bt-reset, li.bt-add",
        function ( e ) {
            var _currentEle = $( this );

            if( _currentEle.is( "div.tr" ) ) {
                var _pk = _currentEle.data("code"),
                    _json = $.param({factor_code: _pk});
                _nutrient.toggleTableOfRows(_url.api.factors, _json,
                    _currentEle);
                if ( _currentEle.is(".sub") ) {
                    var _optedEle = _fListEle.find( "div.opted-item" ),
                        _addEle = _fListEle.find("li.bt-add");
                    _optedEle.load(_url.api.factors + "/" + _pk);
                    if (_addEle.is(".off")) {
                        _addEle.show().removeClass("off").addClass("on");
                    }
                }

            } else if ( _currentEle.is( "li.bt-reset" ) ) {
                _fDetailEle.find("li.bt-get").trigger("click");

            } else if ( _currentEle.is( "li.bt-add" ) ) {
                var _optedFactorCode = _fListEle.find( "div.opted-item" )
                        .data("factorCode"),
                    _nutrientCode = _fDetailEle.find("div.delegate-item")
                        .data("nutrientCode"),
                    _selectedUnitCode = _fListEle
                        .find("select.unit > option:checked" )
                        .data("unitCode"),
                    _inputVal = _fListEle.find( "input#quantity" ).val(),
                    _json = {
                        factor_code: _optedFactorCode,
                        nutrient_code: _nutrientCode,
                        unit_code: _selectedUnitCode,
                        quantity: _inputVal
                    };
                $.post( _url.api.factorSet, _json, function ( data ) {
                    _fDetailEle.load(_url.api.factorSet + "/" + _nutrientCode);
                    _fListEle.find("div.message").text(data);
                });

            }
        });

});
