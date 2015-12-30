$(function() {

	// Alphabet

	$('.coverflow').coverflow();

	$('#first').click(function() {
		$('.coverflow').coverflow('index', 0);
	});

	$('#last').click(function() {
		$('.coverflow').coverflow('index', -1);
	});

	$('#goto6').click(function() {
		$('.coverflow').coverflow('index', 6-1);	// zero-based index!
	});
	
	$('#keyboard').click(function() {
		$('.coverflow').coverflow('option', 'enableKeyboard', $(this).is(':checked'));
	});
	
	$('#wheel').click(function() {
		$('.coverflow').coverflow('option', 'enableWheel', $(this).is(':checked'));
	});
	
	$('#click').click(function() {
		$('.coverflow').coverflow('option', 'enableClick', $(this).is(':checked'));
	});

	/* CD covers */

	if ($.fn.reflect) {
		$('.photos .cover').reflect();
	}

	$('.photos').coverflow({
		duration:		'slow',
		index:			3,
		width:			320,
		height:			240,
		visible:		'density',
		selectedCss:	{	opacity: 1	},
		outerCss:		{	opacity: .1	},
		
		confirm:	function() {
			console.log('Confirm');
		},

		change:		function(event, cover) {
			var img = $(cover).children().andSelf().filter('img').last();
			$('#photos-name').text(img.data('name') || 'unknown');
		}
		
	});	
});
