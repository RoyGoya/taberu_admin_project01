$(document).ready(function () {
    var _navItems = $( "ul#navbar > li > a"),
        _pathName = $(location).attr('pathname');

    !(function (pathName, navItems) {
        $.each( navItems, function (i, item) {
            var _item = $( item );
            if (_item.attr("href") === _pathName) {
                _item.css("background-color", "white");
                _item.css("color", "#2a557f");
            }
        });
    })(_pathName, _navItems);

});