(function($){
	var current_item_id = 0;
	var form = $("##buy-confirmation form");
	$("#thankshop .item .buy").click(function(e){
		current_item_id = $(this).data("item-id");
		$("input[name='item_id']", form).val(current_item_id);
		$("#buy-confirmation").modal("show");
		return false;
	});

	$("#buy-confirmation .accept").click(function(){
		$.ajax({
			url: form.prop('action'),
			type: 'POST',
			data: form.serialize(),
			complete: function(xhr, status){
				catch_notification_messages(xhr);
			}
		});
	});
})(jQuery);
