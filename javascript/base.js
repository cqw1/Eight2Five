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
        redirectStyle($(this).attr('id').split('-').join(' '));
        //redirectStyle($(this).attr('id'));
        return false;
    });

    $('.ef-dropdown-industry').click(function() {
        redirectIndustry($(this).attr('id').split('-').join(' '));
        //redirectIndustry($(this).attr('id'));
        return false;
    });

    $('.ef-dropdown-shop').click(function() {
        redirectShop($(this).attr('id'));
        return false;
    });

    $('#create-account').click(function() {
        window.location.href='/createaccount';
        return false;
    })

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

