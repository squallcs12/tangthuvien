(function($){
    $(".onetime-notification[data-dismiss='alert']").click(function(){
        var key = $(this).data('key');

        var request = {};
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

})(jQuery);

function current_url(){
	this.href = location.origin + location.pathname;
	this.params = this.get_params();
}

current_url.prototype.get_params = function(){
	var params = {};
	if (location.search){
		var search = location.search.substring(1); // remove ? character
		var parts = search.split("&"); // split each param
		for(var i = 0; i < parts.length; i++){
			var part = parts[i];
			var part_split = part.split("=");
			var param_name = part_split.shift();
			var param_value = part_split.join("=");
			params[param_name] = param_value;
		}
	};
	return params;
};

current_url.prototype.remove_param = function(name){
	if(this.params[name]){
		delete this.params[name];
	}
};

current_url.prototype.add_param = function(name, value){
	if(value == null || value == "" || value == undefined){
		this.remove_param(name);
	} else {
		this.params[name] = value;
	}
};

current_url.prototype.generate = function(){
	return this.href + (jQuery.isEmptyObject(this.params) ? '' : '?' + jQuery.param(this.params));
};


(function($){
    var loaded = false;

    function attach_feedback_modal(modal_html){
            $("body").append(modal_html);
            $("#feedback_form").submit(submit_ajax_feedback);
            $("#feedback_modal").modal("show");
    }
    function submit_ajax_feedback(data){
        if(data != "1"){
            $("#feedback_modal").remove();
            attach_feedback_modal(data);
        } else {
            $("#feedback_modal").modal("hide");
        }
    }

    $("#feedback").click(function(e){
        e.preventDefault();
        var _this = this;
        if(!loaded){
            loaded = true; //ignore any unexpected error
            $(this).showLoading();
            $.get($(this).prop('href'), function(form_html){
                $(_this).hideLoading();
                attach_feedback_modal(form_html);            });
        } else {
            $("#feedback_modal").modal("show");
        }
    });
})(jQuery);