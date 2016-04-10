$(document).ready(function() {
    console.log("document ready for style.js");

    $('.ef-shop-button').on('click', function() {
        window.location.href = '/shop?&dress_codes=' + $(this).attr('id');
    })

    $('.ef-occasion-thumbnail').on('click', function() {
        window.location.href = '/shop?&occasion=' + $(this).attr('id').toLowerCase();
    })

    $('.ef-brand').on('click', function() {
        window.location.href = '/shop?&brand=' + $(this).text();
    })


});


function selectIndustry() {
    console.log($("#industry-select option:selected").val());
    console.log($("#industry-select option:selected").text());

    var industry = $("#industry-select option:selected").val();

    window.location.href='/styleguides/industry?industry=' + industry;
}

function selectStyle(img) {
    console.log(img);
    console.log(img.id);
    window.location.href='/styleguides/style?dress_code=' + img.id;
}
