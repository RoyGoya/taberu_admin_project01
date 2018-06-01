$( document ).ready(function () {

    $.taberu = (function() {
        var _urlDict = {
            api: {
                nutrients: "api/nutrients",
                nutrientPattern2: "api/nutrients-pattern2",
                nutrientForm: "api/nutrients-form",
                factors: "/api/factors",
                factorList: "/api/factor-list",
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

            var _foldSubRowsReculsively = function ( targetEle ) {
                $.each(targetEle, function (i, subEle) {
                    subEle = $(subEle);
                    if ( subEle.is( ".on" )) {
                        var subElsSuperCode = subEle.data("code"),
                            subSubEle = subEle.nextAll( "." + subElsSuperCode);
                        _foldSubRowsReculsively(subSubEle);
                        subEle.find("div.bullet").text("➤");
                        subEle.removeClass( "on" ).addClass( "off" );
                    } else {
                        return true;
                    }
                });
                targetEle.hide();
            };

            var _getTemplateAfter = function (url, targetEle,
                                          super_code, subElesColor) {
                $.get(url, function ( template ) {
                    var subEles = $( template ).addClass(super_code);
                    subEles.addClass( "sub" );
                    subEles.css( "background-color", subElesColor );
                    targetEle.after( subEles );
                    console.log( "LoadAfter Complete." );
                });
            };

            var _toggleTableOfRows = function (url, targetEle, subElesColor) {
                subElesColor = subElesColor || "beige";
                if ( targetEle.data("hasSub")==="True") {
                    var _superCode = targetEle.data("code");
                    if ( targetEle.is( ".off" )) {
                        if ( targetEle.is( ".hadCalled" )) {
                            targetEle.nextAll( "." + _superCode ).show();
                        } else {
                            _getTemplateAfter(url, targetEle, _superCode,
                                subElesColor);
                            targetEle.addClass("hadCalled");
                        }
                        targetEle.find("div.bullet").text("∇");
                        targetEle.removeClass( "off" ).addClass( "on" );
                    } else if ( targetEle.is( ".on" )){
                        var _subEls = targetEle.nextAll( "." + _superCode );
                        _foldSubRowsReculsively(_subEls);
                        targetEle.find("div.bullet").text("➤");
                        targetEle.removeClass( "on" ).addClass( "off" );
                    }
                } else {
                    console.log("Current Element have any sub-entities.");
                }
            };
            
            var _loadTemplate = function (url, targetEle, json) {
                if (json === undefined) {
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

            var _replaceTemplate = function (url, targetEle) {
                $.get(url, function (template) {
                    targetEle.replaceWith(template);
                });
            };
            
            var _postSetOfAFactor = function (url, json, doneFunc) {
                $.post( url, json, doneFunc());
            };

            return {
                loadTemplate: _loadTemplate,
                replaceTemplate: _replaceTemplate,
                postSetOfAFactor: _postSetOfAFactor,
                getTemplateAfter: _getTemplateAfter,
                clearCheckedInputs: _clearCheckedInputs,
                toggleTableOfRows: _toggleTableOfRows
            };
        })();

        return {
            url: _urlDict,
            nutrient: _nutrient
        }
    })();
});