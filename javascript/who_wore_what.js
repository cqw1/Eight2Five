// Global interval timer.
var coverflowTimer = setCoverflowTimer();

$(function() {
    $('#left-arrow')
        .click(coverflowPrev)
        .mouseover(function() {
            $('#left-arrow').attr('src', '/images/blackleftarrow.png');
        })
        .mouseout(function() {
            $('#left-arrow').attr('src', '/images/grayleftarrow.png');
        });

    $('#right-arrow')
        .click(coverflowNext)
        .mouseover(function() {
            $('#right-arrow').attr('src', '/images/blackrightarrow.png');
        })
        .mouseout(function() {
            $('#right-arrow').attr('src', '/images/grayrightarrow.png');
        });

    $('#dots-container > *').click(function() {
        $('.photos').coverflow('index', $(this).index());

        clearInterval(coverflowTimer);
        coverflowTimer = setCoverflowTimer();
    })


	$('.coverflow').coverflow();
	
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

        select: function(event, cover, index) {
            // Set everything to be an empty circle and remove their id. 
            // Add selected-dot id and filled circle image to the img at the selected index.
            $('#dots-container > *').attr('src', '/images/emptycircle.png').removeAttr('id').eq(index).attr('id', 'current-dot').attr('src', '/images/filledcircle.png');
        },
		
		confirm: function() {
			console.log('Confirm');
		},

		change:	function(event, cover) {
			var img = $(cover).children().andSelf().filter('img').last();
			$('#photos-name').text(img.data('name') || 'unknown');
		}
		
	});	
});

/** Resets the coverflow timer so that it doesn't change right after the user clicks next or previous. **/
function setCoverflowTimer() {
    // Switches after every 5 milliseconds.
    return setInterval(coverflowNext, 5000);
}

function coverflowNext() {
    // Need to manually check to see if the index actually incremented. If not, then wrap it around to the first picture.
    var previousIndex = $('.photos').coverflow('index');
    $('.photos').coverflow('index', $('.photos').coverflow('index') + 1);
    var newIndex = $('.photos').coverflow('index');

    if (newIndex == previousIndex) {
        $('.photos').coverflow('index', 0);
    }

    clearInterval(coverflowTimer);
    coverflowTimer = setCoverflowTimer();
}

function coverflowPrev() {
    // Automatically wraps around.
    $('.photos').coverflow('index', $('.photos').coverflow('index') - 1);

    clearInterval(coverflowTimer);
    coverflowTimer = setCoverflowTimer();
}

