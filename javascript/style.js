styleInit();


function styleInit() {
    console.log("style.js == styleInit function");
}

function selectIndustry() {
    console.log($("#industry-select option:selected").val());
    console.log($("#industry-select option:selected").text());

    var industry = $("#industry-select option:selected").val();

    window.location.href='/styleguides/industry?industry=' + industry;
}

function selectStyle(img) {
    console.log(img);
    console.log(img.id);
    window.location.href='/styleguides/style?style=' + img.id;
}