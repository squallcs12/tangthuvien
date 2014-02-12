/**
 *
 */
(function($){
    function get_size_in_kb(bytes){
        var kb = parseInt(bytes / 1024);
        return kb + " KB";
    }

    append_new_book_attachment = function (file){
        var file_id = 'book_attachment_' + file['id'];
        $('#' + file_id).remove();
        $("#attachments ul").prepend(
            $("<li></li>").prop('id', file_id).html(
                $("<a></a>")
                    .attr('href', file['url'])
                    .append(
                        $("<span></span>").addClass("filename").html(file['name'])
                    )
                    .append(" ")
                    .append(
                        $("<span></span>").addClass("filesize").html(get_size_in_kb(file['size']))
                    )
                    .append(
                        $("<span></span>").addClass("date").addClass("pull-right").html(file['creation_date'])
                    )
            )
        );
    };
    ajax_upload_book_attachment = function(book_id){
        $('#fileupload').fileupload({
            url: UPLOAD_BOOK_ATTACHMENT_AJAX_URL,
            dataType: 'json',
            formData: {
                book_id: book_id,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            beforeSend: function(){
                $('#upload_attachment .progress').show();
            },
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    append_new_book_attachment(file);
                });
                $('#upload_attachment .progress').hide();
            },
            progressall: function (e, data) {
                var progress = parseInt(data.loaded / data.total * 100, 10);
                $('#upload_attachment .progress .progress-bar').css(
                    'width',
                    progress + '%'
                );
            }
        }).prop('disabled', !$.support.fileInput)
            .parent().addClass($.support.fileInput ? undefined : 'disabled');
        $('#upload_attachment .progress').hide();
    };
})(jQuery);