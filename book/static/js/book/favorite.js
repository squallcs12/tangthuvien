/**
 * 
 */
(function($){
	var loading = false;
	$("#favorite_book").click(function(){
		if(loading){
			return;
		}
		loading = true;
		var request = {};
		request['url'] = SUBMIT_FAVORITE_BOOK_URL;
		request['data'] = {'id' : $(this).data('book_id')};
		request['type'] = 'POST';
		if($(this).attr('favorite') == 'no'){
			var ajaxComplete = function(){
				$("#favorite_book").attr('favorite', 'yes');
				$("#favorite_book").html(LANG_UNFAVORITE);
			}
		} else {
			var ajaxComplete = function(){
				$("#favorite_book").attr('favorite', 'no');
				$("#favorite_book").html(LANG_FAVORITE);
			}
		};
		request['success'] = function(data){
			loading = false;
			$("#favorite_book").removeClass('loading');
			ajaxComplete();
		};
		$("#favorite_book").addClass('loading');
		$.ajax(request);
	});
})(jQuery);