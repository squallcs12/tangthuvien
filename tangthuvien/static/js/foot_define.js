(function($){
	$(".one-time-notification[data-dismiss='alert']").click(function(){
		var key = $(this).data('key');
		
		request = {};
		request['url'] = '{% url "submit_one_time_notification" %}';
		request['type'] = 'post';
		request['data'] = {};
		request['data']['key'] = key;
		
		$.ajax(request);
	});
})(jQuery);
