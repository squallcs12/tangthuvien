var reqModule = reqModule || angular.module('tangthuvien', []);

reqModule.factory('ItemService', function(APIHandler){
    return APIHandler('/thankshop/inventory', {
        list:{method:'GET'},
        get:{method:'GET'}
    });
});

reqModule.factory('APIHandler', function($http, $q){
    function ResourceFactory(url, actions) {
        resources = {};
        angular.forEach(actions, function(action, name) {
            action.method = angular.uppercase(action.method);
            var hasBody = action.method == 'POST' || action.method == 'PUT' || action.method == 'PATCH';
            resources[name] = function(obj, success_fn, failure_fn) {

                var data = {}, params, myurl = url;
                var deferred = $q.defer();

                if (name == 'get') myurl += '/' + name;
                if (obj['id']) {
                    myurl += '/' + obj['id'];
                    delete obj['id'];
                }
                if (name != 'id' && name != 'get') myurl += '/' + name;
                if (obj['target']) {
                    myurl += '/' + obj['target'];
                    delete obj['target'];
                }

                if (hasBody) data = obj;
                else params = obj;

                $http({
                    method:action.method,
                    url:myurl,
                    data: data,
                    params: params,
                    headers: {'Content-Type': 'application/json'}
                }).then(function(resp) {
                    var myobj = resp.data;
                    if (!(resp)) myobj = null;
                    else if (resp[0] === "" || resp[0] === "\"") myobj = [];
                    (success_fn||angular.noop)(myobj);
                    deferred.resolve(myobj);
                }, failure_fn);
                return deferred.promise;
            };
        });
        return resources;
    }
    return ResourceFactory;
});


function InventoryController($scope, ItemService){
    $scope.items = [];

    $scope.fetchItems = function(){
        ItemService.list({id: "me"}, function(items){
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

