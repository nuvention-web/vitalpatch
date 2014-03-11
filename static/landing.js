$(document).ready(function() {
	// $('form').delay(500).animate({'left': '50%', 'margin-left': -$('form').width()/2 });

	function animWeight(val) {
		if ($("#weight").css("display") == "none") {
			if (val.toLowerCase() == "spay" || val.toLowerCase() == "neuter") {  // If not visible and we need weight
				$("#weight").css("display", "inline").animate({"width": "170px", "padding": "6px"});
			}
		}
		else {
			if (val.toLowerCase() != "spay" && val.toLowerCase() != "neuter") {  // If visible and we don't need weight
				$("#weight").animate({"width": "0px", "padding": "0px"}, function() {
					$(this).css("display", "none");
				});
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
	$("#procedure").autocomplete({
		source: procedures
	});

	// Animate weight field on keyup and autocomplete select
	$("#procedure").keyup(function() {
		animWeight($(this).val());
	}); 
	$("#procedure").on("autocompleteselect", function(event, ui) {
		animWeight(ui.item.label);
	});


	// Animate search bar to the top
	// NOTE: not used right now; waiting on finalizing design for results page
	// $("form").submit(function(e) {
	// 	var top = parseInt($("#bar").css("top"), 10);
	// 	$("#bar").animate({"top": top+20}, function() {
	// 		$(this).animate({"top": 0, "margin-top": 0}, function() {
	// 			$("form").unbind("submit").submit();
	// 		});
	// 	});
	// 	return false;
	// });

	// Make sure all form fields are filled
	$("form").submit(function(e) {
		var empty = $(this).find('input').filter(function() {
			return this.value == "";
		});
		if (empty.length > 0) {
			shouldAlert = true;
			if ($("#weight").css("display") == "none") {
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
});