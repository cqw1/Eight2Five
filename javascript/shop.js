globalFilters = [];
globalDefaultSort = 'defaultSort';
globalDefaultItems = 'defaultItems';
globalDefaultPage = 0;
globalNumPages = 1;

$(document).ready(function() {
    console.log('shop.js document ready');

    argDict = createArgDict();

    console.log('argDict ');
    console.log(argDict);

    updateCheckboxes(argDict);

    // Filters. 
    $('.ef-gender-filter').change(function() {
        var argType = 'gender';
        var argValue = $(this).attr('id');
        var checked = $(this).prop('checked');

        argDict = updateArgDictCheckbox(argType, argValue, checked, argDict);
        delete argDict['page'];
        updateUrl(argDict);
    })

    $('.ef-article-filter').change(function() {
        var argType = 'article';
        var argValue = $(this).attr('id');
        var checked = $(this).prop('checked');

        argDict = updateArgDictCheckbox(argType, argValue, checked, argDict);
        delete argDict['page'];
        updateUrl(argDict);
    })

    // Sorts.
    $('.ef-sort-option').on('click', function(event) {
        event.preventDefault();
        var argType = 'sort';
        var argValue = $(this).text().toLowerCase().replace(/ /g, "%20");

        argDict = updateArgDictDropdownAndUrl(argType, argValue, argDict);
    })

    // Display number of items on a page.
    $('.ef-items-option').on('click', function(event) {
        event.preventDefault();
        var argType = 'items';
        var argValue = $(this).text().toLowerCase();

        argDict = updateArgDictDropdownAndUrl(argType, argValue, argDict);
    })

    // Page.
    $('.ef-page-option').on('click', function(event) {
        event.preventDefault();
        var argType = 'page';
        var argValue = $(this).text();

        argDict = updateArgDictDropdownAndUrl(argType, argValue, argDict);
    })

    $('#ef-prev-page').on('click', function(event) {
        event.preventDefault();
        var currentPage = parseInt($('#ef-current-page').text());
        if (currentPage == 2) {
            delete argDict['page'];
            updateUrl(argDict);
        } else if (currentPage > 2) {
            argDict['page'] = [currentPage - 1];
            updateUrl(argDict);
        }
    })

    $('#ef-next-page').on('click', function(event) {
        console.log('next page');
        event.preventDefault();
        var currentPage = parseInt($('#ef-current-page').text());
        console.log('currentpage: ' + currentPage);

        if (currentPage < globalNumPages) {
            console.log('entered if statement');
            argDict['page'] = [currentPage + 1];
            updateUrl(argDict);
        }
    })


});

// Creates arg dictionary from current url.
function createArgDict() {
    args = window.location.search.substring(1).split('&');
    argDict = {};

    for (var i = 0; i < args.length; i++) {
        // Filter out empty strings.
        if (args[i].length > 0) {
            var pair = args[i].split('=');
            var key = pair[0];
            var value = pair[1];

            if (key in argDict) {
                argDict[key].push(value);
            } else {
                argDict[key] = [value];
            }
        }
    }

    return argDict;
}

// Set checkboxes and dropdowns from previous user selections. Info from url args.
function updateCheckboxes(argDict) {
    console.log('in updateCheckboxes');
    for (var key in argDict) {
        var filters = argDict[key];
        for (var i in filters) {
            if (globalFilters.indexOf(filters[i]) > -1) {
                // Checkbox arg and not a dropdown arg.
                $('#' + filters[i]).prop('checked', true);
            }
        }
    }
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

function updateArgDictDropdownAndUrl(argType, argValue, argDict) {
    if (argType in argDict) {
        // Should only have one value.
        var value = argDict[argType][0];

        if (value == argValue) {
            // Value already selected. Do nothing.
            console.log('value already selected');
        } else if (argValue == globalDefaultItems || argValue == globalDefaultSort || argValue == globalDefaultPage) {
            // Selected default. remove whatever is currently applied.
            delete argDict[argType];
            if (argType != 'page') {
                delete argDict['page'];
            }
            updateUrl(argDict);
        } else {
            // Change to new selection.
            argDict[argType] = [argValue];
            if (argType != 'page') {
                delete argDict['page'];
            }
            updateUrl(argDict);
        }
    } else if (argValue == globalDefaultItems || argValue == globalDefaultSort || argValue == globalDefaultPage) {
        // Selected default and no selection is currently applied. Do nothing.
        console.log('selected default.');
    } else {
        // Want to apply a new selection.
        argDict[argType] = [argValue];
        if (argType != 'page') {
            delete argDict['page'];
        }
        updateUrl(argDict);
    }

    return argDict;
}

// Construct new url from arg dictionary and redirects there. 
function updateUrl(argDict) {
    var url = window.location.origin + window.location.pathname + '?';

    for (var key in argDict) {
        var values = argDict[key];
        for (var i in values) {
            url += '&' + key + '=' + values[i];
        }
    }
    window.location.href = url;
}

function initGlobals(filters, defaultSort, defaultItems, defaultPage, numPages) {
    for (var i in filters) {
        globalFilters = globalFilters.concat(filters[i].selections);
    }

    globalDefaultSort = defaultSort.replace(/ /g, '%20');
    globalDefaultItems = defaultItems;
    globalDefaultPage = defaultPage;
    globalNumPages = numPages.length

    console.log(globalDefaultSort);
    console.log(globalDefaultItems);
    console.log(globalDefaultPage);

}


