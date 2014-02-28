var reqModule = reqModule || angular.module('tangthuvien', ANGULAR_REQUIRES);

reqModule.factory('ShopItemService', function(APIHandler){
    return APIHandler('/thankshop/item', {
        list:{method:'GET'},
        get:{method:'GET'}
    });
});

function ShopItemController($scope, ShopItemService, $sanitize){
    $scope.items = [];

    $scope.fetchItems = function(){
        ShopItemService.list({}, function(items){
            $scope.items = items;
        });
    };

    $scope.fetchItems();

    var $ = jQuery;
    $scope.showBuyForm = function($item){
        $scope.item = $item;
		$("#buy-confirmation").modal("show");
    };
}

(function($){
	var current_item_id = 0;
	var form = $("#buy-confirmation form");
	$("#thankshop .item .buy").click(function(e){
		current_item_id = $(this).data("item_id");
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
			},
			success: function(data){
				$("#buy-confirmation").modal("hide");
			}
		});
	});
})(jQuery);
