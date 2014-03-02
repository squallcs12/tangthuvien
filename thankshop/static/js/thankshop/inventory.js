var reqModule = reqModule || angular.module('tangthuvien', ANGULAR_REQUIRES);

reqModule.factory('InventoryService', function(APIHandler){
    return APIHandler('/thankshop/inventory', {
        list:{method:'GET'},
        get:{method:'GET'}
    });
});

function InventoryController($scope, InventoryService){
    $scope.items = [];

    $scope.fetchItems = function(){
        InventoryService.list({}, function(items){
            $scope.items = items;
        });
    };

    $scope.fetchItems();

    var $ = jQuery;
    $scope.showDetail = function($item){
        $scope.item = $item;
        $("#item_information").modal("show");
    };
}

