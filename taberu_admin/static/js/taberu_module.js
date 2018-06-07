$( document ).ready(function () {

    // Extend jQuery: make shortcuts for PUT and DELETE
    $.each( ["put", "delete" ], function ( i, method ) {
        $[ method ] = function ( url, data, callback, type ) {
            if ( $.isFunction( data ) ) {
                type = type || callback;
                callback = data;
                data = undefined;
            }

            return $.ajax({
                url: url,
                type: method,
                dataType: type,
                data: data,
                success: callback
            });
        };
    });

    // Module Pattern
    // https://learn.jquery.com/code-organization/concepts/
    $.taberu = (function() {
        var _urlDict = {
            api: {
                nutrients: "api/nutrients",
                nutrientSet: "api/nutrient-set",
                nutrientPattern2: "api/nutrient-pattern2",
                nutrientForm: "api/nutrient-form",
                nutrientOption: "api/nutrient-option",
                factors: "/api/factors",
                factorSet: "/api/factor-set",
                tags: "/api/tags"
            },
            view: {

            }
        };

        var _common = (function () {
           var _coloringATableOfRow = function (targetEle, before, after) {
                targetEle.prevAll(".opted").removeClass("opted")
                    .css("background-color", before);
                targetEle.nextAll(".opted").removeClass("opted")
                    .css("background-color", before);
                if (targetEle.not(".opted")) {
                    targetEle.addClass( "opted" );
                    targetEle.css( "background-color", after );
                }
           };

           return {
               coloringATableOfRow: _coloringATableOfRow
           };
        })();

        var _nutrient = (function() {
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

            var _toggleTableOfRows = function (url, json, targetEle, subElesColor) {
                subElesColor = subElesColor || "beige";
                targetEle.css( "background-color", "paleturquoise");
                if ( targetEle.data("hasSub")==="True") {
                    var _superCode = targetEle.data("code");
                    if ( targetEle.is( ".off" )) {
                        if ( targetEle.is( ".hadCalled" )) {
                            targetEle.nextAll( "." + _superCode ).show();
                        } else {
                            $.get(url, json, function ( template ) {
                                var subEles = $( template ).addClass(_superCode);
                                subEles.addClass( "sub" );
                                subEles.css( "background-color", subElesColor );
                                targetEle.after( subEles );
                                console.log( "LoadAfter Complete." );
                            });
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

            return {
                toggleTableOfRows: _toggleTableOfRows
            };
        })();

        return {
            url: _urlDict,
            common: _common,
            nutrient: _nutrient
        }
    })();
});