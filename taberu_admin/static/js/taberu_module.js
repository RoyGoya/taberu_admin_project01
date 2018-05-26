$( document ).ready(function () {

    $.taberu = (function() {
        var _urlDict = {
            nutrient: {
                detail: "/api/nutrient/detail",
                list: "/api/nutrient/list",
                pattern2: "/api/nutrient/pattern2"

            },
            factor: {
                detail: "/api/factor/detail",
                list: "/api/factor/list",
                select: "/api/factor/select"
            },
            tag: {

            }
        };

        var _nutrient = (function() {
            var _clearCheckedInputEls = function (inputEls) {
                inputEls.each(function (idx) {
                    inputEls.eq(idx).prop("checked", false);
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

            var _toggleListOfEls = function (targetEle, paramData, subElesColor) {
                subElesColor = subElesColor || "beige";
                if ( targetEle.data("hasSub")==="True") {
                    var _superCode = targetEle.data("code");
                    if ( targetEle.is( ".off" )) {
                        if ( targetEle.is( ".hadCalled" )) {
                            targetEle.nextAll( "." + _superCode ).show();
                        } else {
                            _getTemplateAfter(_urlDict.factor.list,
                                targetEle, paramData, _superCode, subElesColor);
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
            
            var _loadTemplate = function (url, targetEle, paramData) {
                targetEle.load(url, paramData, function () {
                        console.log("Load Templete Complete.");
                });
            };

            var _replaceTemplate = function (url, targetEle, paramData) {
                $.get(url, paramData, function (template) {
                    targetEle.replaceWith(template);
                });
            };
            
            var _getTemplateAfter = function (url, targetEle, paramData,
                                          super_code, subElesColor) {
                $.get(url, paramData, function ( template ) {
                    var subEles = $( template ).addClass(super_code);
                    subEles.addClass( "sub" );
                    subEles.css( "background-color", subElesColor );
                    targetEle.after( subEles );
                    console.log( "LoadAfter Complete." );
                });
            };
            
            var _getNutrientPattern2 = function(url, pattern1Val) {
                $.ajax({
                    url: url,
                    data: {
                        pattern1: pattern1Val
                    },
                    type: "GET",
                    dataType: "json"
                })
                    .done(function ( jsonDataSet ) {
                        var targetEl = $("ul#pattern2").empty();

                        for (idx in jsonDataSet) {
                            var li = $('<li>'),
                                input = $('<input>').attr({
                                    name: "pattern2", type: "radio",
                                    value: jsonDataSet[idx]}),
                                label = $('<label>').text(idx);

                            targetEl.append(li.append(input).append(label))
                        }
                        console.log( "Nutrient-Type2 is Successfully Loaded!" );
                    })
                    .fail(function( xhr, status, errorThrown ) {
                        alert( "Sorry, there was a problem!" );
                        console.log( "Error: " + errorThrown );
                        console.log( "Status: " + status );
                        console.dir( xhr );
                    });
            };

            return {
                loadTemplate: _loadTemplate,
                replaceTemplate: _replaceTemplate,
                getTemplateAfter: _getTemplateAfter,
                clearCheckedInputEls: _clearCheckedInputEls,
                getNutrientPattern2: _getNutrientPattern2,
                toggleListOfEls: _toggleListOfEls
            };
        })();

        return {
            url: _urlDict,
            nutrient: _nutrient
        }
    })();
});