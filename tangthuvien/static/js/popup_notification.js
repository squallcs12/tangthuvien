/**
 *
 */
(function($){
	catch_notification_messages = function(xhr){
		var messages = xhr.getResponseHeader("messages");
		if(messages){
			messages = JSON.parse(messages);
			popup_notification(messages);
		}
	};
	popup_notification = function (messages_pool){
		for(var key in messages_pool){
			var messages = messages_pool[key];
			for(var i = 0; i < messages.length; i++){
				add_message(key, messages[0]);
			}
		}
		$("#popup-notification").modal("show");
	};

	function add_message(key, message){
		if(key == 'error'){
			key = 'danger';
		}
		$("#popup-notification .modal-body").append(
			'<div class="row notifications">' +
	            '<div class="col-lg-12">' +
	                '<div class="alert alert-' + key + '">' +
	                    '<p>' +
	                        message +
	                    '</p>' +
	                '</div>' +
	            '</div>' +
	        '</div>'
		);
	}
})(jQuery);

(function($){
	$("#popup-notification").on("hidden.bs.modal", function(){
		 $(".modal-body", this).html("");
	});
})(jQuery);