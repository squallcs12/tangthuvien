/**
 * Main js for read page
 */

function apply_reading_section_config($, configStyles){
	var cookieStyles = $.cookie('config_reading_section_styles');
	if(!cookieStyles){
		cookieStyles = configStyles;
		$.cookie('config_reading_section_styles', configStyles);
	}
	var styles = cookieStyles.split(';');
	var contentDiv = $("#chapter .content");
	for(var i = 0; i < styles.length; i++){
		var styleParts = styles[i].split(':');
		contentDiv.css(styleParts[0], styleParts[1]);
	}
};


function attach_thank_button($, chapter_id, submit_thank_url){
	var thankButton = $("#chapter-thank .thank-button");
	var thankCountDiv = $("#chapter-thank .count");
	var thankCount = parseInt(thankCountDiv.text());
	function thank(event){
		thankButton
			.unbind('click', thank)
			.removeClass('btn-default')
			.addClass('btn-disable');
		var request = {};
		request['url'] = submit_thank_url;
		request['data'] = {};
		request['data']['chapter_id'] = chapter_id;
		request['type'] = 'POST';
		request['success'] = function(data){
			console.log(data);
			thankButton.removeClass('loading');
		};
		thankButton.addClass('loading');
		$.ajax(request);

		thankCountDiv.html(thankCount + 1);
	}
	if(!thankButton.hasClass('btn-disable')){
		thankButton.click(thank)
	}
};