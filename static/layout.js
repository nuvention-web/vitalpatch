var overlayShowing = false;

$(document).ready(function() {

	// Show about
	$(".bottom-link").click(function() {
		if (!overlayShowing) {
			var overlayId = $(this).attr("id");
			$("#" + overlayId + "-overlay").fadeIn();
			overlayShowing = true;
		}
	});

	// Fade out overlay
	$(".x-button").click(function() {
		$(this).parent().fadeOut();
		overlayShowing = false;
	});
});