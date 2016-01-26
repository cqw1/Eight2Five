$(document).ready(function() {
    console.log("document ready for industry.js");

    $('.ef-shop-button').on('click', function() {
        var ids = $(this).attr('id').split('-');
        window.location.href = '/shop?&industries=' + ids[0] + '&styles=' + ids[1] ;
    })

});


function selectIndustry() {
	console.log($("#industry-select option:selected").val());
	console.log($("#industry-select option:selected").text());

	var industry = $("#industry-select option:selected").val();

	window.location.href='/styleguides/industry?industry=' + industry;
}

function shopTheLook() {
	console.log('industry.js == shopTheLook function');
}
