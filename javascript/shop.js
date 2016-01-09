$(document).ready(function() {
    console.log('shop.js document ready');
    console.log(getUrlArgsDict());


    // Filters. Capitalization is to match the display name of the filter type in the python dictionary.
    $('.ef-Gender-filter').change(function() {
        addUrlArg('gender', $(this).attr('id'));
    })
    $('.ef-Article-filter').change(function() {
        addUrlArg('article', $(this).attr('id'));
    })

    // Sorts.
    $('.ef-items-option').on('click', function() {
        addUrlArg('items', $(this).text());
    })

    // Display number of items on a page.
    $('.ef-sort-option').on('click', function() {
        addUrlArg('sort', $(this).text());
    })
});

function getUrlArgsDict() {
    args = window.location.search.substring(1).split('&');

    dict = {};

    for (var i = 0; i < args.length; i++) {
        // Filter out empty strings.
        if (args[i].length > 0) {
            var pair = args[i].split('=');
            var key = pair[0];
            var value = pair[1];

            if (key in dict) {
                dict[key].push(value);
            } else {
                dict[key] = [value];
            }
        }
    }
    
    return dict;
}

function addUrlArg(argType, argValue) {
    var url = window.location.href;

    if (url.indexOf('?') < 0) {
        url += '?';
    }

    url += '&' + argType + '=' + argValue;

    window.location.href = url;
}


