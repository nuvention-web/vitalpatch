$(document).ready(function() {
	$('form').delay(500).animate({'left': '50%', 'margin-left': -$('form').width()/2 });

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
		source: procedures
	});
});