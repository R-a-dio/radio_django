$(document).ready(function () {
    var settings = {
        pagesSelector: '.page_link',
        pageSelector: '.endless_page_template',
        onClick: function (context) {
            var state = {
                action: 'search_page',
                key: context.key,
                url: context.url
            }
                
            window.history.pushState(state, null, context.url);
        }
    };

    $.endlessPaginate(settings);

    $(window).bind('popstate', function (event) {
        if (event.state.action !== 'search_page') { return; }

        var context = event.state;
        var data = 'querystring_key=' + context.key;

        $(settings.pageSelector).load(context.url, data);    
    });
});
