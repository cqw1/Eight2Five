globalArgDict = {};
globalFilters = [];

$(document).ready(function() {

    console.log('shop.js document ready');
    console.log('globalArgDict before');
    console.log(globalArgDict);

    createArgDict();

    console.log('globalArgDict after');
    console.log(globalArgDict);

    updateCheckboxes();



    // Filters. Capitalization is to match the display name of the filter type in the python dictionary.
    $('.ef-gender-filter').change(function() {
        var argType = 'gender';
        var argValue = $(this).attr('id');
        var checked = $(this).prop('checked');

        updateArgDictCheckbox(argType, argValue, checked, globalArgDict);


        //addUrlArg(argType, argValue);
    })

    $('.ef-article-filter').change(function() {
        var argType = 'article';
        var argValue = $(this).attr('id');

        addUrlArg(argType, argValue);
    })

    // Sorts.
    $('.ef-items-option').on('click', function() {
        var argType = 'items';
        var argValue = $(this).text();

        addUrlArg(argType, argValue);
    })

    // Display number of items on a page.
    $('.ef-sort-option').on('click', function() {
        var argType = 'sort';
        var argValue = $(this).text();

        addUrlArg(argType, argValue);
    })
});

// Modifies global globalArgDict value.
function createArgDict() {
    args = window.location.search.substring(1).split('&');

    for (var i = 0; i < args.length; i++) {
        // Filter out empty strings.
        if (args[i].length > 0) {
            var pair = args[i].split('=');
            var key = pair[0];
            var value = pair[1];

            if (key in globalArgDict) {
                globalArgDict[key].push(value);
            } else {
                globalArgDict[key] = [value];
            }
        }
    }
}

function updateCheckboxes() {
    

}

// arg (e.g. 'gender=Men')
function argExists(arg) {
    return (window.location.search.indexOf(arg) > -1);
}

// remove arg if checked is false. insert if checked is true.
// returns upated arg dictionary.
function updateArgDictCheckbox(argType, argValue, checked, argDict) {
    if (argType in argDict) {
        var values = argDict[argType];

        // TODO: array.indexOf not supported in IE8 and earlier.
        var index = values.indexOf(argValue);

        if (index > -1) {
            // Args contains value.
            if (!checked) {
                // Unchecked checkbox. Need to remove value.
                values.splice(index, 1);
            } else {
                // Checked checkbox. Shouldn't happen, but could be inconsistent state.
                // Do nothing. Similar to a refresh.
                console.log('shop.updateArgDictCheckbox: error with url args');
                //window.location.href = window.location.href;
            }
        } else {
            // Arg doesn't contain value.
            if (!checked) {
                // Inconsistent state - refresh.
                console.log('shop.updateArgDictCheckbox: error with url args');
                //window.location.href = window.location.href;
            } else {
                values.push(argValue);
            }
        }
    } else {
        // Arg not in dictionary.
        if (checked) {
            // Add arg type and value to dict.
            argDict[argType] = [argValue];
        } else {
            // Inconsistent state - refresh.
            console.log('shop.updateArgDictCheckbox: error with url args');
        }
    }

    console.log('shop.updateArgDictCheckbox:');
    console.log(argDict);
    return argDict;
}

function addUrlArg(argType, argValue) {
    var url = window.location.href;

    if (url.indexOf('?') < 0) {
        url += '?';
    }

    url += '&' + argType + '=' + argValue;

    window.location.href = url;
}

function initFilters(filters) {
    for (var i in filters) {
        globalFilters = globalFilters.concat(filters[i].selections);
    }

    console.log('new global filters: ');
    console.log(globalFilters);
}


