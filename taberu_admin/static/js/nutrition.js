$(document).ready(function () {

    var _nutrition = {};

    _nutrition._getNutritionPreview = function(dtPatternVal, ntPattern1Val) {
        $.ajax({
            url: "/api/nutrition/nutritionlist",
            data: {
                "dtPattern": dtPatternVal,
                "ntPattern1": ntPattern1Val
            },
            type: "GET",
            dataType: "json"
        })
            .done(function ( jsonDataList ) {
                var targetEl = $("section#tb-preview"),
                    cntEl = $("div#cnt-preview"),
                    header = $('<header>');

                header.append($('<div>').text('Code'))
                    .append($('<div>').text('EngName'))
                    .append($('<div>').text('HasSub'));
                targetEl.empty().append(header);

                jsonDataList.forEach(function (jsonData, index) {
                   if(index===0) {
                       cntEl.text(jsonData.cnt);
                   } else {
                       var tr = $('<div>').attr("class", "tr-preview"),
                           dtPattern = jsonData.dt_pattern,
                           ntPattern1 = jsonData.nt_pattern1,
                           ntPattern2 = jsonData.nt_pattern2,
                           serial = jsonData.serial,
                           code = "",
                           engName = jsonData.eng_name,
                           isSet = jsonData.is_set,
                           style = {};

                       code += (dtPattern + ntPattern1 + ntPattern2 + serial);
                       tr.attr({
                           "data-dt-pattern": dtPattern,
                           "nt-pattern1": ntPattern1,
                           "nt-pattern2": ntPattern2,
                           "serial": serial
                       });
                       tr.append($('<div>').text(code))
                           .append($('<div>').text(engName));
                       if(isSet) {
                           isSet = "True";
                           style = { style: "color:green" };
                       } else {
                           isSet = "False";
                           style = { style: "color:lightblue" };
                       }
                       (function (style, target) {
                           target.append($('<div>').attr(style).text(isSet));
                       }(style, tr));
                        targetEl.append(tr);
                   }
                });
                console.log( "Nutrition-Preview is Successfully Loaded!" );
            })
            .fail(function( xhr, status, errorThrown ) {
                alert( "Sorry, there was a problem!" );
                console.log( "Error: " + errorThrown );
                console.log( "Status: " + status );
                console.dir( xhr );
            });
    };

    _nutrition._getNutritionType2 = function(ntPattern1Val) {
        $.ajax({
            url: "/api/nutrition/getntpattern2",
            data: {
                ntPattern1: ntPattern1Val
            },
            type: "GET",
            dataType: "json"
        })
            .done(function ( jsonDataSet ) {
                var targetEl = $("ul#nt_pattern2").empty();

                for (idx in jsonDataSet) {
                    var li = $('<li>'),
                        input = $('<input>').attr({
                            name: "nt_pattern2", type: "radio",
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

    _nutrition._clearCheckedInputEls = function (inputEls) {
        inputEls.each(function (idx) {
            inputEls.eq(idx).prop("checked", false);});
    };

    // Jquery Custom Events
    // https://learn.jquery.com/events/introduction-to-custom-events/
    $( "li#box-selection" ).on("click", "ul#dt_pattern > li > input, " +
        "ul#nt_pattern1 > li > input, ul#nt_pattern2 > li > input",
        function (event) {
            var _currentEle = $( this ),
                _dtEle = $( "ul#dt_pattern" ),
                _nt1Ele = $( "ul#nt_pattern1" ),
                _nt2Ele = $( "ul#nt_pattern2" );

            if ( _currentEle.is( "ul#dt_pattern > li > input" ) ) {
                var _dtPatternVal = _currentEle.val(),
                    _dtInputs = $( "ul#dt_pattern").find( "input" ),
                    _ntInputs = $( "ul#nt_pattern1" ).find( "input" );
                _nutrition._clearCheckedInputEls(_dtInputs);
                _currentEle.prop("checked", true);
                _nutrition._clearCheckedInputEls(_ntInputs);
                $( "ul#nt_pattern2" ).empty();
                _nutrition._getNutritionPreview(_dtPatternVal);
            } else if ( _currentEle.is( "ul#nt_pattern1 > li > input" ) ) {
                var dtPatternVal = _dtEle.find( "input:checked" ).val(),
                    ntPattern1Val = _currentEle.val(),
                    ntInputs = _nt1Ele.find( "input" );
                _nutrition._clearCheckedInputEls(ntInputs);
                $(this).prop("checked", true);
                _nutrition._getNutritionPreview(dtPatternVal, ntPattern1Val);
                _nutrition._getNutritionType2(ntPattern1Val);
            } else if ( _currentEle.is( "ul#nt_pattern2 > li > input" ) ) {
                console.log("nt2");
            }
        });

    $( "li#box-preview" ).on("click", "div.tr-preview",
        function ( event ) {
            var _currentEle = $( this ),
                _boxSelecEle = $( "li#box-selection" );

            if ( _currentEle.is( "div.tr-preview" )) {
                var _dtPatternVal = _currentEle.data("dtPattern"),
                    _ntPattern1Val = _currentEle.data("ntPattern1"),
                    _ntPattern2Val = _currentEle.data("ntPattern2"),
                    _serial = _currentEle.data("serial"),
                    _dataSet = {
                        dt_pattern: _dtPatternVal,
                        nt_pattern1: _ntPattern1Val,
                        nt_pattern2: _ntPattern2Val,
                        serial: _serial
                    },
                    _paramData = $.param(_dataSet);

                _boxSelecEle.load('/api/nutrition/formtemplate', _paramData,
                    function () {
                        console.log("success!");
                    }
                );
            }
        });
});
