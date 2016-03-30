$(document).ready(function() {
});

// Global interval timer.
var coverflowTimer = setCoverflowTimer();

$(function() {
    $('.ef-look-thumbnail').click(function() {
        window.location.href = '/whoworewhat/look?id=' + $(this).attr('id');
    });

    // Coverflow stuff below =====================
    
    $('#ef-left-arrow')
        .click(coverflowPrev)
        .mouseover(function() {
            $('#ef-left-arrow').attr('src', '/images/blackleftarrow.png');
        })
        .mouseout(function() {
            $('#ef-left-arrow').attr('src', '/images/grayleftarrow.png');
        });

    $('#ef-right-arrow')
        .click(coverflowNext)
        .mouseover(function() {
            $('#ef-right-arrow').attr('src', '/images/blackrightarrow.png');
        })
        .mouseout(function() {
            $('#ef-right-arrow').attr('src', '/images/grayrightarrow.png');
        });

    $('#ef-dots-container > *').click(function() {
        $('.photos').coverflow('index', $(this).index());

        clearInterval(coverflowTimer);
        coverflowTimer = setCoverflowTimer();
    })

	if ($.fn.reflect) {
		$('.photos .cover').reflect();
	}

	$('.photos').coverflow({
		duration:		'slow',
		index:			1,
		width:			312,
		height:			312,
		visible:		'density',
		selectedCss:	{	opacity: 1	},
		outerCss:		{	opacity: .1	},

        select: function(event, cover, index) {
            // Set everything to be an empty circle and remove their id. 
            // Add selected-dot id and filled circle image to the img at the selected index.
            $('#ef-dots-container > *').attr('src', '/images/emptycircle.png').removeAttr('id').eq(index).attr('id', 'ef-current-dot').attr('src', '/images/filledcircle.png');
        },
		
		confirm: function(event, cover, index) {
			console.log('Confirm');
            var img = $(cover).children().andSelf().filter('img').last();
            window.location.href = '/whoworewhat/person?person=' + img.attr('data-name');
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

