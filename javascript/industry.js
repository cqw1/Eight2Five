industryInit();


function industryInit() {
	console.log("industry.js == industryInit function");
}

function selectIndustry() {
	console.log($("#industry-select option:selected").val());
	console.log($("#industry-select option:selected").text());

	var industry = $("#industry-select option:selected").val();

	window.location.href='/styleguides/industry?industry=' + industry;
}