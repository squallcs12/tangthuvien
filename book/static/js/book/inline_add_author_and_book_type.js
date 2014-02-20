/**
 *
 */
function inline_add_author_and_type(form_id){
    try{
        jQuery.fn.modalmanager.defaults.resize = true;
    } catch(e){

    }

    (function($){
        var new_author_option = document.createElement('option');
        $(new_author_option)
            .html(STR_CREATE_NEW)
            .prop('value', '-1');
        $('#new-author-form-div').on('hide.bs.modal', function(){
            $("#" + form_id + " select[name='author']").val('');
            $("#" + form_id + " select[name='author']").change();
        });

        (function(){
            function replaceCkeditor(){
                $('#new-author-form-div').off('shown.bs.modal', replaceCkeditor);
                $('#new-author-form-div textarea').each(function(){

                CKEDITOR.replace(this, {
                    "filebrowserWindowWidth": 940,
                    "toolbar_Basic": [["Styles", "Format", "Bold", "Italic", "Underline"]],
                    "toolbar_Full": [
                        ["Styles", "Format", "Bold", "Italic", "Underline"],
                        ["Image", "Flash", "Table", "HorizontalRule"],
                        ["TextColor", "BGColor"],
                        ["Smiley", "SpecialChar"],
                        ["Source"]],
                    "filebrowserUploadUrl": "/ckeditor/upload/",
                    "height": 150,
                    "width": "100%",
                    "filebrowserBrowseUrl": "/ckeditor/browse/",
                    "skin": "moono",
                    "filebrowserWindowHeight": 725,
                    "toolbar": "Basic"});
                });
            }
            $('#new-author-form-div').on('shown.bs.modal', replaceCkeditor);
        })();

        $("#" + form_id + " select[name='author']").change(function(){
            if($(this).val() == '-1'){
                $('#new-author-form-div').modal('show'); //it seem that the modal was destroyed and re-created
            }
        });
        $("#" + form_id + " select[name='author'] option:first").after(new_author_option);
        $("#new-author-form").submit(function(){
            var _this = this;
            var ajaxConf = {}
            ajaxConf['url'] = ADD_BOOK_AUTHOR_AJAX_URL;
            ajaxConf['data'] = $(this).serialize();
            ajaxConf['type'] = 'POST';
            ajaxConf['success'] = function(data){
                if(data['success']){
                    var added = false;
                    var new_option = document.createElement('option');
                    $(new_option)
                        .prop('value', data['id'])
                        .html(data['name']);

                    $("#" + form_id + " select[name='author'] option").slice(2).each(function(){
                        if(added){
                            return;
                        }
                        if($(this).html() > data['name']){
                            added = true;
                            $(this).before(new_option);
                        }
                    });
                    if(!added){
                        $("#" + form_id + " select[name='author']").append(new_option);
                    }

                    // hide modal first
                    $('#new-author-form-div').modal('hide');
                    $("#" + form_id + " select[name='author']").val(data['id']);
                }
            };
            ajaxConf['complete'] = function(){
                $("[type='submit'] img.loading", _this).remove();
            };
            $("[type='submit']", _this).append(LOADING_IMAGE_HTML);
            $.ajax(ajaxConf);
            return false;
        });

        var new_type_option = document.createElement('option');
        $(new_type_option)
            .html(STR_CREATE_NEW)
            .prop('value', '-1');
        $('#new-type-form-div').on('hide.bs.modal', function(){
            $("#" + form_id + " select[name='ttv_type']").val('');
            $("#" + form_id + " select[name='ttv_type']").change();
        });
        $("#" + form_id + " select[name='ttv_type']").change(function(){
            if($(this).val() == '-1'){
                $('#new-type-form-div').modal('show');
            }
        });
        $("#" + form_id + " select[name='ttv_type'] option:first").after(new_type_option);
        $("#new-type-form").submit(function(){
            var _this = this;
            var ajaxConf = {}
            ajaxConf['url'] = ADD_BOOK_TYPE_AJAX_URL;
            ajaxConf['data'] = $(this).serialize();
            ajaxConf['type'] = 'POST';
            ajaxConf['success'] = function(data){
                if(data['success']){
                    var added = false;
                    var new_option = document.createElement('option');
                    $(new_option)
                        .prop('value', data['id'])
                        .html(data['name']);

                    $("#" + form_id + " select[name='ttv_type'] option").slice(2).each(function(){
                        if(added){
                            return;
                        }
                        if($(this).html() > data['name']){
                            added = true;
                            $(this).before(new_option);
                        }
                    });
                    if(!added){
                        $("#" + form_id + " select[name='ttv_type']").append(new_option);
                    }

                    // hide modal first
                    $('#new-type-form-div').modal('hide');
                    $("#" + form_id + " select[name='ttv_type']").val(data['id']);
                }
            };
            ajaxConf['complete'] = function(){
                $("[type='submit'] img.loading", _this).remove();
            };
            $("[type='submit']", _this).append(LOADING_IMAGE_HTML);
            $.ajax(ajaxConf);
            return false;
        });
    })(jQuery);
};