init();


function init() {
	console.log("in init function");
}

function selectIndustry() {
	console.log($("#industry-select option:selected").val());
	console.log($("#industry-select option:selected").text());

	var e = document.getElementById("industry-select");
	console.log(e.options[e.selectedIndex].text);

	window.location.href='/home';
}