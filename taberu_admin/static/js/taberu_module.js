$( document ).ready(function () {

    $.taberu = (function() {
        var _urlDict = {
            nutrition: {
                detail: "/api/nutrition/detail",
                list: "/api/nutrition/list",
                pattern2: "/api/nutrition/pattern2",
                factor: {
                    detail: "/api/nutrition/factor/detail",
                    list: "/api/nutrition/factor/list"
                }
            },
            tag: {

            }
        };

        var _nutrition = (function() {

            var _loadTemplate = function (url, targetEle) {
                targetEle.load(url, function () {
                        console.log("Load Templete Complete.")
                    });
                };

            var _loadTemplate = function (url, targetEle, paramData) {
                targetEle.load(url, paramData, function () {
                        console.log("Load Templete Complete.")
                    });
                };

            var _clearCheckedInputEls = function (inputEls) {
                inputEls.each(function (idx) {
                    inputEls.eq(idx).prop("checked", false);});
            };

            var _getNutritionPattern2 = function(url, pattern1Val) {
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
                        console.log( "Nutrition-Type2 is Successfully Loaded!" );
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
                clearCheckedInputEls: _clearCheckedInputEls,
                getNutritionPattern2: _getNutritionPattern2
            };
        })();

        return {
            url: _urlDict,
            nutrition: _nutrition
        }
    })();
});