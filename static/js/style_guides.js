$(document).ready(function() {
    console.log("styleguides.js document ready"); 

    $('.ef-dress-code-image').on('click', function() {
        window.location.href='/styleguides/style?dress_code=' + $(this).attr('id');
    })

    $('.ef-industry-thumbnail').on('click', function() {
        window.location.href='/styleguides/industry?industry=' + $(this).attr('id');
    })

});
