/**
 * Main js for index page
 */
(function ($){
	filter_books_by_category = function (selectedCategories, categories) {
        $("input[name='categories']").tagsinput({
            itemValue: 'id',
            itemText: 'title',
        });
        $("input[name='categories']").tagsinput('input').typeahead({
            val: {},
            display: 'title',
            source: categories,
            template: '<p>{{text}}</p>',
            itemSelected: function(obj){
                $("input[name='categories']").tagsinput('add', obj);
                $("input[name='categories']").tagsinput('input').val('');
                $("input[name='categories']").tagsinput('focus');
            }
        })

        for(var category_id in selectedCategories){
	        $("input[name='categories']").tagsinput('add', {
	            'id': category_id,
	            'title': selectedCategories[category_id]
	        });
        }
        $("input[name='categories']").change(function(){
            reload_book_list_by_category(this);
        });
    };

    var loading = false;
    var current_ajax_request = null;
    function reload_book_list_by_category(filter){
        if (loading){
            current_ajax_request.abort();
        }
        var ajaxSettings = {}
        ajaxSettings['url'] = AJAX_LIST_BOOK_URL;
        ajaxSettings['data'] = {};
        ajaxSettings['data']['categories'] = $(filter).val();
        ajaxSettings['success'] = function(data){
            updateBookList(data);
            $("#books_list_block").removeLoading();
            if (typeof window.history.pushState != 'undefined'){
                window.history.pushState(data,"", data['url']);
            } else {
                alert("Not implemented yet");
            }

        }
        loading = true;
        $("#books_list_block").putLoading();
        current_ajax_request = $.ajax(ajaxSettings);
    }
    $(window).on("popstate", function(e){
    	var data = e.originalEvent.state;
    	if(data){
    		updateBookList(data);
    	} else {
    		// TODO: implement back to home
    	}
    });
    function updateBookList(data){
    	$("#books_list_block").html(data['content']);
        $('title').html(data['title']);
    }
})(jQuery);