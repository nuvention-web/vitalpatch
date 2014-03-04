$(document).ready(function() {
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