/**
 * Main js file for book app
 */

function copy_book_process($, process_output_url){
    var start = 0;
    var end = 0;
    var total_chapter = 0;
    var page_percent = 0;
    var chapter_num = 0;
    var each_page_percent = 1;
    function change_percent(percent){
        $("#process_bar .progress-bar").css('width', percent + '%');
        $("#process_bar .progress-bar").html(percent + '%');
    }

    // process command from log
    function report_copy_process(command){

    	//split command parts
        var args = command.split(' ');

        //first part is command name
        switch(args[0]){
            case 'start':
               	start = parseInt(args[1]);
               	break;
            case 'end':
               	end = parseInt(args[1]);
               	each_page_percent = (100 / (end - start + 1)).toFixed(2);
               	break;
			case 'process_page':
				var page = parseInt(args[1]) - 1;
				if(page == 100){
					$("#process_output").html('');
				}
				var total = end - start + 1;
				page_percent = ((page * 100 + 0.0) / total).toFixed(2);
				change_percent(page_percent);
				chapter_num = 0;
				break;
            case 'total_chapter':
               	total_chapter = parseInt(args[1]);
               	break;
            case 'skip_post':
            case 'process_chapter':
                chapter_num += 1;
               	var chapter_percent = ((chapter_num * each_page_percent) / total_chapter ).toFixed(2);
               	var current_percent = (parseFloat(page_percent) + parseFloat(chapter_percent)).toFixed(2);
               	change_percent(current_percent);
               	break;
            case 'finish':
            	clearInterval(interval_process);
               	$("#process_bar").removeClass('active');
               	$("#process_bar .progress-bar")
                   .removeClass('progress-bar-info')
                   .addClass('progress-bar-success');
               	change_percent(100.00);
               	break;
            default:
               break;
        }
   		$("#process_output").append(command + "\n");
    }

    // constructure ajax request
	var start_line = 0;
	var ajaxConf = {};
	ajaxConf['url'] = process_output_url;
	ajaxConf['data'] = {}
	ajaxConf['success'] = function(data){
		if (!data){
			return;
		}
		var lines = data.split("\n");
		start_line += lines.length;
		for (var i = 0; i < lines.length; i++){
			var line = lines[i];
			report_copy_process(line);
			if (line == 'finish'){
				clearInterval(interval_process);
			}
		}
        $("#process_output").scrollTop($("#process_output")[0].scrollHeight);
	}

	// request new log every 1 second
    var interval_process = setInterval(function(){
    	ajaxConf['data']['start_line'] = start_line;
    	$.ajax(ajaxConf);
    }, 1000);
};