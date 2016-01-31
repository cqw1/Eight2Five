globalFilters = [];
globalDefaultSort = 'defaultSort';
globalDefaultItems = 'defaultItems';
globalDefaultPage = 0;
globalNumPages = 1;

$(document).ready(function() {
    console.log('shop.js document ready');
    argDict = createArgDict();

    updatePageNumber(argDict);


    // Page.
    $('.etf-page-option').on('click', function(event) {
        event.preventDefault();
        var argType = 'page';
        var argValue = $(this).text();

        argDict = updateArgDictDropdownAndUrl(argType, argValue, argDict);
    })

    $('.etf-prev-page').on('click', function(event) {
        event.preventDefault();
        var currentPage = parseInt($('.ef-current-page').text());
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
        var currentPage = parseInt($('.ef-current-page').text());

        console.log($('.ef-current-page').text());

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
        console.log(page);
        console.log(li_pages.get(3));
        li_pages.get(3).addClass('active');

    } else {
        li_pages.get(1).addClass('active');

    }
}
