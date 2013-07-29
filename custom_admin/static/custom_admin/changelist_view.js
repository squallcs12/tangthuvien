django.jQuery(function($){
	function product_search_query(){
		params = {}
		$(".filter_column").each(function(){
			if(value = $(this).val().trim()){
				params[this.name] = value;
			}
		});
		params = $.param(params)
		location.href = '?' + params
	}
	$("input[type=text].filter_column").keydown(function(event){
		if(event.which == 13){
			product_search_query();
			return false;
		}
	});
});