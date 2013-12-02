/**
 * 
 */
(function($){
    $("#config-reading-section-form select").change(function(){
        // save config in cookie
        var cssAttribute = $(this).data('css-name');
        var cssValue = $(this).val();
        var cssStatement = cssAttribute + ":" + cssValue;
        var cookieStyles = $.cookie('config_reading_section_styles');
        var styles = cookieStyles.split(';');
        var found = false;
        for(var i = 0; i < styles.length; i++){
            var style = styles[i].split(':');
            if(style[0] == cssAttribute){
                styles[i] = cssStatement;
                found = true;
                break;
            }
        }        
        if(!found){
            styles.push(cssStatement);
        }
        var cookieStyles = styles.join(";");
        $.cookie('config_reading_section_styles', cookieStyles);
        // end save config 
        
        $("#chapter .content").css(cssAttribute, cssValue);
    });
    $("#config-reading-section-form").submit(function(){
        var ajaxConf = {}
        ajaxConf['url'] = AJAX_BOOK_READING_CONFIG_URL;
        ajaxConf['data'] = $(this).serialize();
        ajaxConf['type'] = 'POST';
        ajaxConf['complete'] = function(){
            $("#config-modal").modal("hide");
            $("#config-reading-section-form button[type=submit] .loading").remove();
        }
        $("#config-reading-section-form button[type=submit]").append(LOADING_IMAGE_HTML);
        $.ajax(ajaxConf);
        return false;
    });
    $("#config-reading-section-form button[type=reset]").click(function(){
        $("#config-reading-section-form")[0].reset();
        $("#config-reading-section-form select").change();
    });
    
})(jQuery);