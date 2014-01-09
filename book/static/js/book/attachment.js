/**
 * 
 */
jQuery(function($){
	var ajaxConf = {};
	ajaxConf['url'] = APPROVE_BOOK_ATTACHMENT_AJAX_JS;
	ajaxConf['data'] = {};
	$("#attachments .approve").click(function(){
		var _this = this;
		ajaxConf['success'] = function(data){
			if(data['status'] == 'success'){
				$(_this).remove();
			} else {
				alert(data['message']);
			}
		}
		ajaxConf['data']['attachment_id'] = $(this).data('attachment_id');
		$.ajax(ajaxConf);
		return false;
	});
});