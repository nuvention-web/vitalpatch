// Check the radio button with the given animal
function checkRadioButton(animal) {
	$('input[name=animal]').each(function() {
		if ($(this).val() == animal) {
			$(this).prop('checked', true);
			return;
		}
	});
}