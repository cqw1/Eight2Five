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

});

