function animWeight(val) {
	if ($("#weight-control-group").css("display") == "none") {
		if (val.toLowerCase() == "spay" || val.toLowerCase() == "neuter") {  // If not visible and we need weight
			$("#weight-control-group").fadeIn();
		}
	}
	else {
		if (val.toLowerCase() != "spay" && val.toLowerCase() != "neuter") {  // If visible and we don't need weight
			$("#weight-control-group").fadeOut();
		}
	}
}

var procedures = [
	"Domestic Health Certificate",
	"International Health Certificate",
	"Annual Wellness Check",
	"Rabies (1 year)",
	"Rabies (3 years)",
	"Lyme Disease",
	"Bordetella",
	"Heartworm Testing",
	"DHLPP",
	"Leptospirosis",
	"Fecal Exam",
	"Spay",
	"Neuter"
];
$( "#procedure" ).autocomplete({
	source: procedures,
	select: function(event, ui) {
		animWeight(ui.item.label);
	}
});

// Animate weight field
$("#procedure").keyup(function() {
	animWeight($(this).val());
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