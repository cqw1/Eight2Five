$(document).ready(function() {
    console.log("styleguides.js document ready"); 

    $('.ef-style-image').on('click', function() {
        window.location.href='/styleguides/style?style=' + $(this).attr('id');
    })

});
