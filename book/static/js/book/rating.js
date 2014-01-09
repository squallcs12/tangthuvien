/**
 * 
 */
(function($){
	$("#book_rating .rate-star button").click(function(){
		var clickedButton = this;
		rateNumber = $(this).data('rate-number');

		$("#book_rating .rate-star button").attr('disabled', true);
		resultSpan = $("#book_rating .average-result");
		countSpan = $("#book_rating .rating-count");

		ratingCount = parseInt(countSpan.html());

		var newResult = (ratingCount * parseFloat(resultSpan.html()) + rateNumber) / (ratingCount + 1);
		newResult = newResult.toFixed(2);

		resultSpan.html(newResult);
		countSpan.html(ratingCount + 1);

		request = {};
		request['url'] = SUBMIT_BOOK_RATING_URL;
		request['type'] = 'POST';
		request['data'] = {};
		request['data']['number'] = rateNumber;
		request['data']['book_id'] = $(this).data('book_id');
		request['success'] = function(data){
			resultSpan.html(data['average_result'].toFixed(2));
			countSpan.html(data['rating_count']);
			$(clicked_button).removeClass('loading');
		}
		$(clickedButton).addClass('loading');
		$.ajax(request);
	});
})(jQuery);