$(document).ready(function() {
    console.log('base.js document ready'); 

    // Handle dropdowns

    $('.etf-dropdown-shop').click(function() {
        redirectShop($(this).attr('id'));
        return false;
    });

});

function redirectStyle(arg) {
    window.location.href='/styleguides/style?style=' + arg;
}

function redirectIndustry(arg) {
    window.location.href='/styleguides/industry?industry=' + arg;
}

function redirectShop(arg) {
    window.location.href='/shop?&article=' + arg;
}

