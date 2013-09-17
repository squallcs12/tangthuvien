(function($){
	$(".onetime-notification[data-dismiss='alert']").click(function(){
		var key = $(this).data('key');

		request = {};
		request['url'] = ONETIME_NOTIFICATION_SUBMIT_URL;
		request['type'] = 'post';
		request['data'] = {};
		request['data']['key'] = key;
		
		$.ajax(request);
	});
})(jQuery);
