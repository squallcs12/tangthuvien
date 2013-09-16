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
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/')
			|| (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin
					+ '/') ||
			// or any other URL that isn't scheme relative or absolute i.e
			// relative.
			!(/^(\/\/|http:|https:).*/.test(url));
}

jQuery.ajaxSetup({
	beforeSend : function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			xhr.setRequestHeader("X-CSRFToken", jQuery.cookie('csrftoken'));
		}
	}
});
function get_real_link(link){
    var a = document.createElement('a');
    a.href = link;
    link = a.href;
    delete a;
    return link;
}
jQuery(document).on("click", "ul.pagination li.disabled a", function(){
	return false;
});