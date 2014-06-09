$(document).ready(function() {
	// Toggle sort/filter option visibility
	$('#hide-sort-button').click(function() {
		if ($('#sort-container').css('display') == 'none') {
			$('#sort-container').slideDown();
			$(this).text('Hide sort and filter options');
		}
		else {
			$('#sort-container').slideUp();
			$(this).text('Show sort and filter options');
		}
	});

	// Set default sort/filter options
	// Clear value of hidden sort/filter fields in form, then submit form
	$('#default-sort-button').click(function() {
		var names = ['sort', 'radius', 'rating'];
		names.forEach(function(name) {
			$('#search-form input[name="' + name + '"]').val('');
		});			
		$('#search-form').submit();
	});

	// Change sort/filter options
	$('.sort-options-radio').change(function () {		
		var name = $(this).attr('name');  // Get the name of the just clicked option
		var value = $(this).val();		  // Get the value of the just clicked option		

		var $form = $('#search-form');
		$form.find('input[name="' + name + '"]').val(value);  // Set the correct hidden field in the form
		$form.submit(); // Submit form
	});
});

function checkSortRadios(sort, radius, rating) {	
	$('.sort-options-radio[name="sort"][value="' + sort + '"]').prop('checked', true);
	$('.sort-options-radio[name="radius"][value="' + radius + '"]').prop('checked', true);
	$('.sort-options-radio[name="rating"][value="' + rating + '"]').prop('checked', true);
}