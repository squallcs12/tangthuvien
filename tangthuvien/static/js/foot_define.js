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

	$("body").on("shown.bs.modal", "div.modal.modal-centered", function(){
		$(this).css("top", jQuery(window).height() / 2 - $(this).height() / 2);
	});
	$("body").on("hidden.bs.modal", "div.modal.modal-centered", function(){
		$(this).css("top", "");
	});

	$.fn.showLoading = function(){
		$(this).each(function(){
			$(this).append(LOADING_IMAGE_HTML);
		});
	};

	$.fn.removeLoading = function(){
		$(this).each(function(){
			$(".loading", this).remove();
		});
	};
})(jQuery);
