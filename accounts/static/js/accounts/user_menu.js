jQuery(function(){
    var $ = jQuery;

    var opened_links = [];
    var opened_menu = $.cookie("user_openned_menu");
    if (opened_menu){
        opened_links = opened_menu.split(";");
    }

    $("#userMenu .panel-heading a").each(function(){
        var this_link = $(this).prop("href");
        if(opened_links.indexOf(this_link)!==-1){
            $(this).click();
        }
    });

    $("#userMenu .panel-heading a").click(function(e){
        var this_link = $(this).prop("href");

        var found = opened_links.indexOf(this_link);

        if(found===-1){
            opened_links.push(this_link);
        } else {
            opened_links.splice(found, 1);
        }
        opened_menu = opened_links.join(";");

        var date = new Date();
        date.setTime(date.getTime() + (8 * 60 * 60 * 1000));
        $.cookie("user_openned_menu", opened_menu, {path: '/', expires: date});
    });
});