/**
 *
 */
function generate_prc_socket_io(book_id){
	if(typeof(socket) == 'undefined'){
		socket = io.connect(SOCKET_IO_URL);
	}
	(function($){

		socket.on('generate_book_prc_' + book_id, function(data){
			console.log(data);
			$("#generate_book_prc_div .progress .progress-bar").addClass('progress-bar-success');
			$("#generate_book_prc_div .progress .progress-bar").html(LANG_PRC_IS_GENERATED);
			append_new_book_attachment(data.attachment);
			setTimeout(function(){
				$("#generate_book_prc_div .progress").fadeOut();
			}, 1000);
		});

		$("#generate_book_prc").click(function(){
			$("#generate_book_prc_div .progress .progress-bar").html(LANG_PRC_IS_GENERATING);
			$("#generate_book_prc_div .progress .progress-bar").removeClass('progress-bar-success');
			$("#generate_book_prc_div .progress").show();
			socket.emit('generate_book_prc', { book_id: book_id });
			return false;
		});
		$("#generate_book_prc").removeClass('disabled');
	})(jQuery);
};