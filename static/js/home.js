$(document).ready(function() {
    console.log('home.js document ready'); 

    // Subscribe Modal
    $(window).load(function(){
	  setTimeout(function(){
	      $('#subscribeModal').modal('show');
	  }, 10000);
	});
});
