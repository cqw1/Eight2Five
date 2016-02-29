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
    $('.ef-dropdown-dress-code').click(function() {
        redirectStyle($(this).attr('id').split('-').join(' '));
        return false;
    });

    $('.ef-dropdown-industry').click(function() {
        redirectIndustry($(this).attr('id').split('-').join(' '));
    });

    $('.ef-dropdown-shop').click(function() {
        redirectShop($(this).attr('id'));
        return false;
    });

    // Handle social media icons.
    $('#ef-facebook-icon').click(function() {
        window.location.href = 'https://www.facebook.com/skirttheceiling'
    });
    $('#ef-twitter-icon').click(function() {
        window.location.href = 'https://www.twitter.com/skirttheceiling'
    });
    $('#ef-instagram-icon').click(function() {
        window.location.href = 'https://www.instagram.com/skirttheceiling'
    });

});

function redirectStyle(arg) {
    window.location.href='/styleguides/style?dress_code=' + arg;
}

function redirectIndustry(arg) {
    window.location.href='/styleguides/industry?industry=' + arg;
}

function redirectShop(arg) {
    window.location.href='/shop?&apparels=' + arg;
}

