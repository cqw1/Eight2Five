globalFilters = [];
globalDefaultSort = 'defaultSort';
globalDefaultItems = 'defaultItems';
globalDefaultPage = 0;
globalNumPages = 1;

$(document).ready(function() {
    console.log('shop.js document ready');
    argDict = createArgDict();

    updatePageNumber(argDict);

    // Sorts.
    $('.etf-sort-option').on('change', function(event) {
        event.preventDefault();
        console.log('etf-sort-option clicked');
        var argType = 'sort';
        var argValue = $('.etf-sort-option option:selected').text().toLowerCase().replace(/ /g, '%20');
        console.log(argValue);
        argDict = updateArgDictDropdownAndUrl(argType, argValue, argDict);
    })

    // Number of items on a page.
    $('.etf-items-option').on('change', function(event) {
        event.preventDefault();
        console.log('etf-items-option clicked');
        var argType = 'items';
        var argValue = $('.etf-items-option option:selected').text().toLowerCase();
        console.log(argValue);
        argDict = updateArgDictDropdownAndUrl(argType, argValue, argDict);
    })

    // Page.
    $('.etf-page-option').on('click', function(event) {
        event.preventDefault();
        var argType = 'page';
        var argValue = $(this).text();

        argDict = updateArgDictDropdownAndUrl(argType, argValue, argDict);
    })

    $('.etf-prev-page').on('click', function(event) {
        event.preventDefault();
        var currentPage = parseInt($('.etf-current-page').text());
        if (currentPage == 2) {
            delete argDict['page'];
            updateUrl(argDict);
        } else if (currentPage > 2) {
            argDict['page'] = [currentPage - 1];
            updateUrl(argDict);
        }
    })

    $('.etf-next-page').on('click', function(event) {
        console.log('next page');
        event.preventDefault();
        var currentPage = parseInt($('.etf-current-page').text());

        console.log($('.etf-current-page').text());

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

function updatePageNumber(argDict) {
    console.log('in updatePageNumber');
    var li_pages = $('.pagination > ul > li');
    if ('page' in argDict) {
        var page = parseInt(argDict['page']);
        $(li_pages.get(page)).addClass('active');
        $(li_pages.get(page)).addClass('etf-current-page');

    } else {
        $(li_pages.get(1)).addClass('active');
        $(li_pages.get(1)).addClass('etf-current-page');

    }
}

function setSortOption(selectedSort) {
    console.log(selectedSort);
    $('.etf-sort-option option:contains("' + selectedSort + '")').prop('selected', true);
    console.log($('.etf-sort-option option:eq(1)').selected);
}

function setItemOption(selectedItemsPerPage) {
    $('.etf-items-option option:contains("' + selectedItemsPerPage + '")').prop('selected', true);
    console.log($('.etf-items-option option:eq(1)').selected);
}
