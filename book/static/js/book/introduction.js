(function($){
	$(function(){
		$("#languages .language").click(function(){
			var _this = this;
			$(this).showLoading();
			$.ajax({
				type: "POST",
				url: BOOK_LANGUAGE_PREFERENCE_URL,
				data: {
						book_id: $("#book").data("item_id"),
						language_id: $(this).data("id")
					},
				success: function(){
					$(_this).removeLoading();

					// remove old language preference
					$("#languages .language.btn-success")
						.removeClass("btn-success")
						.addClass("btn-default");

					// set current language as preference
					$(_this).removeClass("btn-default")
							.addClass("btn-success");
				}
			});
		});
	});
})(jQuery);
