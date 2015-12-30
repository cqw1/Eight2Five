$(function() {
	// Alphabet

    $('#left-arrow')
        .click(function() {
            // Automatically wraps around.
            $('.photos').coverflow('index', $('.photos').coverflow('index') - 1);
        })
        .mouseover(function() {
            $('#left-arrow').attr('src', '/images/blackleftarrow.png');
        })
        .mouseout(function() {
            $('#left-arrow').attr('src', '/images/grayleftarrow.png');
        });

    $('#right-arrow')
        .click(function() {
            // Need to manually check to see if the index actually incremented. If not, then wrap it around to the first picture.
            var previousIndex = $('.photos').coverflow('index');
            $('.photos').coverflow('index', $('.photos').coverflow('index') + 1);
            var newIndex = $('.photos').coverflow('index');

            if (newIndex == previousIndex) {
                $('.photos').coverflow('index', 0);
            }
        })
        .mouseover(function() {
            $('#right-arrow').attr('src', '/images/blackrightarrow.png');
        })
        .mouseout(function() {
            $('#right-arrow').attr('src', '/images/grayrightarrow.png');
        });


	$('.coverflow').coverflow();
	
	$('#keyboard').click(function() {
		$('.coverflow').coverflow('option', 'enableKeyboard', $(this).is(':checked'));
	});
	
	$('#wheel').click(function() {
		$('.coverflow').coverflow('option', 'enableWheel', $(this).is(':checked'));
	});
	
	$('#click').click(function() {
		$('.coverflow').coverflow('option', 'enableClick', $(this).is(':checked'));
	});

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


