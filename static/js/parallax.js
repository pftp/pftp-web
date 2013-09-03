(function($) {

	$.fn.parallax = function(options) {

		var settings = $.extend({ speed: 0.8, top: 0},
			options);

		var selector = $(this).selector;
		var is_load = true;
		var is_init = true;

		$(window).scroll(function(e) {
			if (is_load) load();
			update_background();
			update_text();
		});

		function load() {
			settings.top = -$(window).scrollTop();
			is_load = false;
		}

		function init(top) {
			settings.top -= top;
			is_init = false;
		}

		function update_background() {
			var scrolled = $(window).scrollTop();
			if ($(selector).offset().top - scrolled > window.innerHeight) return;
			var scroll_dist = scrolled * settings.speed;
			var position = scroll_dist - $(selector).offset().top;
			if (is_init) init(position);
			$(selector).css('background-position', "0px " + (position + settings.top) + "px");
		}

		function update_text() {
			$(selector + ' *').each(function() {
				var window_pos = $(this).offset().top - $(window).scrollTop();
				if (window_pos < 100) {
					$(this).css('opacity', window_pos/100.0);
				} else if (window_pos < 280) {
					$(this).css('opacity', 1.0);
				} else {
					$(this).css('opacity', (400-window_pos)/100.0);
				}
			});
		}
		return selector;
	};

	$('.bg1').parallax();
	$('.bg2').parallax({speed:0.2});
	$('.bg3').parallax();
	$('.bg4').parallax();
	$('.bg5').parallax();
	$('.bg6').parallax();

})(jQuery);