styleGuidesInit();


function styleGuidesInit() {
	console.log("styleguides.js == styleGuidesInit function");
}

function selectIndustry() {
	console.log($("#industry-select option:selected").val());
	console.log($("#industry-select option:selected").text());

	var industry = $("#industry-select option:selected").text();

	window.location.href='/styleguides/industry?industry=' + industry;
}