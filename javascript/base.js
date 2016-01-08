$(document).ready(function() {
    console.log('base.js document ready'); 

    // Update active tab on navbar.
    var pathname = window.location.pathname.split("/")[1];

    $('.navbar li.active').removeClass('active');

    var validPaths = ['whoworewhat', 'styleguides', 'shop'];
    if (validPaths.indexOf(pathname) > -1) {
        // In the array.
        var id = '#' + pathname;
        $(id).addClass('active');
    } else {
        $("#home").addClass('active');
        console.log('caught empty');
    }


    // Handle dropdowns
    $('.ef-dropdown-style').click(function() {
        redirectStyle($(this).text());
        return false;
    });

    $('.ef-dropdown-industry').click(function() {
        redirectIndustry($(this).text());
        return false;
    });

    $('.ef-dropdown-shop-men').click(function() {
        redirectShopMen($(this).text());
        return false;
    });

    $('.ef-dropdown-shop-women').click(function() {
        redirectShopWomen($(this).text());
        return false;
    });
});

function redirectStyle(arg) {
    window.location.href='/styleguides/style?style=' + arg;
}

function redirectIndustry(arg) {
    window.location.href='/styleguides/industry?industry=' + arg;
}

function redirectShopMen(arg) {
    window.location.href='/shop?gender=Men&type=' + arg;
}

function redirectShopWomen(arg) {
    window.location.href='/shop?gender=Women&type=' + arg;
}
