$(document).ready(function() {
    console.log("styleguides.js document ready"); 

    $('.ef-style-image').on('click', function() {
        window.location.href='/styleguides/style?style=' + $(this).attr('id');
    })

    $('.ef-industry-thumbnail').on('click', function() {
        window.location.href='/styleguides/industry?industry=' + $(this).attr('id');
    })

});
