function update_background() {
	var scrolled = $(window).scrollTop();
	var scroll_rate = -scrolled * 0.2;
	if (scroll_rate > 40) scroll_rate = 40 + scroll_rate;
	$('.parallax_block').css('background-position', "0% " + (scroll_rate));
}

function check_text() {
	$('.parallax_block p').each(function() {
		var window_pos = $(this).offset().top - $(window).scrollTop();
		if (window_pos < 80) {
			$(this).css('opacity', window_pos/100.0);
		} else if (window_pos < 280) {
			$(this).css('opacity', 1.0);
		} else {
			$(this).css('opacity', (400-window_pos)/100.0);
		}
	});
}

$(window).scroll(function(e) {
	update_background();
	check_text();
});