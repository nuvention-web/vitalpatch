// Only show weight group when a surgery is selected
$('#procedure').change(function() {
	var $procedureSelect = $('select[name=procedure] option:selected'); 

	if ($procedureSelect.parent().attr('label') == 'Surgery') {
		$("#weight-control-group").fadeIn();
	}

	else {
		$("#weight-control-group").fadeOut();
	}
});

// Make sure all form fields are filled
$("form").submit(function(e) {
	var empty = $(this).find('input').filter(function() {
		return this.value == "";
	});
	if (empty.length > 0) {
		shouldAlert = true;
		if ($("#weight-control-group").css("display") == "none") {
			console.log(empty[0]);
			console.log($("#weight").get(0));
			if (empty[0] == $("#weight").get(0) && empty.length == 1) {
				shouldAlert = false;
			}
		}

		if (shouldAlert) {
			alert("Please fill in all fields.");
			return false;
		}
	}
});

// Automatically choose the procedure option based on previous selection
function initialSelection(value) {
	$('#procedure').val(value);
}

// Send feedback form email
$("#barometer_tab").removeAttr('onclick').attr({
	'href': '#feedbackModal',
	'data-toggle': 'modal'
}).click(function() {
	$("#feedback-submit").fadeIn();
	$(".flash").fadeOut();
	$("#feedback-form").find('input').val('');
	$("#feedback-form").find('textarea').val('');
});

$("#feedback-form").submit(function() {
	$.post(
		"feedback", 
		{
			'email': $(this).find('input[name="email"]').val(),
			'subject': $(this).find('input[name="subject"]').val(),
			'description': $(this).find('textarea[name="description"]').val(),
		}, 
		function(data) {
		   	$("#feedbackModal .modal-body").prepend(
		   		"<div class='flash'>" + data.message + "</div>"
		   	);
    	}, 
    	'json');
	return false;
});

$("#feedback-submit").click(function() {
	$("#feedback-form").submit();
	$(this).fadeOut();
});