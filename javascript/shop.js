$(document).ready(function() {
    console.log('shop.js document ready');


    $('#Men').change(function() {
        console.log('#Men change; prop: ');
        console.log($('#Men').prop('checked'));
    })

    $('.ef-items-option').on('click', function() {
        console.log($(this).text())
    })



});