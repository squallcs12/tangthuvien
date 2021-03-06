function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host;
    // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e
    // relative.
    !(/^(\/\/|http:|https:).*/.test(url));
}

(function($) {
    $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
        if (!csrfSafeMethod(options.type) && sameOrigin(options.url)) {
            if(typeof(options.headers) == 'undefined'){
                options.headers = {};
            }
            options.headers["X-CSRFToken"] = $.cookie('csrftoken');
        }
    });
})(jQuery);

function get_real_link(link) {
    var a = document.createElement('a');
    a.href = link;
    link = a.href;
    delete a;
    return link;
}


jQuery(document).on("click", "ul.pagination li.disabled a", function() {
    return false;
});
jQuery(document).on("click", "ul.pagination li.active a", function() {
    return false;
});

jQuery(document).ajaxSuccess(function( event, xhr, settings ) {
    catch_notification_messages(xhr);
});