/**
 * Main js for read page
 */

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
		request['error'] = function(xhr){
			thankButton
			.bind('click', thank)
			.removeClass('btn-disable')
			.addClass('btn-default');
			catch_notification_messages(xhr);
			thankCountDiv.html(thankCount);
		};
		thankButton.addClass('loading');
		$.ajax(request);

		thankCountDiv.html(thankCount + 1);
	}
	if(!thankButton.hasClass('btn-disable')){
		thankButton.click(thank);
	}
};

(function($){
	$("#form_chapter_jump").submit(function(e){
		e.preventDefault();
		location.href = $(this).prop("action").replace("000999000", $("input[name='page']").val());
		return false;
	});
})(jQuery);
