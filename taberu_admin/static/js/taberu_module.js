$( document ).ready(function () {

    $.taberu = (function() {
        var _urlDict = {
            api: {
                nutrients: "api/nutrients",
                nutrientPattern2: "api/nutrient-pattern2",
                factors: "/api/factors",
                factorSet: "/api/factor-set",
                tags: "/api/tags"
            },
            view: {

            }
        };

        var _nutrient = (function() {
            var _clearCheckedInputs = function (elements) {
                elements.each(function (idx) {
                    elements.eq(idx).prop("checked", false);
                });
            };

            var _foldSubElesReculsively = function ( targetEle ) {
                $.each(targetEle, function (i, subEle) {
                    subEle = $(subEle);
                    if ( subEle.is( ".on" )) {
                        var subElsSuperCode = subEle.data("code"),
                            subSubEle = subEle.nextAll( "." + subElsSuperCode);
                        _foldSubElesReculsively(subSubEle);
                        subEle.find("div.bullet").text("➤");
                        subEle.removeClass( "on" ).addClass( "off" );
                    } else {
                        return true;
                    }
                });
                targetEle.hide();
            };

            var _toggleListOfEls = function (targetEle, json, subElesColor) {
                subElesColor = subElesColor || "beige";
                if ( targetEle.data("hasSub")==="True") {
                    var _superCode = targetEle.data("code");
                    if ( targetEle.is( ".off" )) {
                        if ( targetEle.is( ".hadCalled" )) {
                            targetEle.nextAll( "." + _superCode ).show();
                        } else {
                            _getTemplateAfter(_urlDict.factors, targetEle,
                                json, _superCode, subElesColor);
                            targetEle.addClass("hadCalled");
                        }
                        targetEle.find("div.bullet").text("∇");
                        targetEle.removeClass( "off" ).addClass( "on" );
                    } else if ( targetEle.is( ".on" )){
                        var _subEls = targetEle.nextAll( "." + _superCode );
                        _foldSubElesReculsively(_subEls);
                        targetEle.find("div.bullet").text("➤");
                        targetEle.removeClass( "on" ).addClass( "off" );
                    }
                } else {
                    console.log("Current Element have any sub-entities.");
                }
            };
            
            var _loadTemplate = function (url, targetEle, json) {
                if (json === null) {
                    targetEle.load(url, function () {
                        console.log("Load Templete Complete.");
                    });
                } else {
                    var _queryStr = $.param( json );
                    targetEle.load(url, _queryStr, function () {
                        console.log("Load Templete Complete.");
                    });
                }
            };

            var _replaceTemplate = function (url, targetEle, json) {
                var _queryStr = $.param( json );
                $.get(url, _queryStr, function (template) {
                    targetEle.replaceWith(template);
                });
            };
            
            var _getTemplateAfter = function (url, targetEle, json,
                                          super_code, subElesColor) {
                var _queryStr = $.param( json );
                $.get(url, _queryStr, function ( template ) {
                    var subEles = $( template ).addClass(super_code);
                    subEles.addClass( "sub" );
                    subEles.css( "background-color", subElesColor );
                    targetEle.after( subEles );
                    console.log( "LoadAfter Complete." );
                });
            };

            return {
                loadTemplate: _loadTemplate,
                replaceTemplate: _replaceTemplate,
                getTemplateAfter: _getTemplateAfter,
                clearCheckedInputs: _clearCheckedInputs,
                toggleListOfEls: _toggleListOfEls
            };
        })();

        return {
            url: _urlDict,
            nutrient: _nutrient
        }
    })();
});