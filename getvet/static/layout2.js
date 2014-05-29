/***********************************************/
/*                 Dropdowns                   */
/***********************************************/
// Format animal dropdown with image and name
function formatAnimalDropdown(animal) {
    return '<img class="animal-dropdown-img" src="static/imgs/Animal Buttons/' + animal.text + '.png">' + ' ' + animal.text;
}

// Format animal selection with image and name
function formatAnimalSelected(animal) {
	return '<img class="animal-selected-img" src="static/imgs/Animal Buttons/' + animal.text + '.png">' + '  ' + animal.text;
}

// Make dropdowns select2
$(document).ready(function() {
	$('#animal').select2({
		escapeMarkup: function(m) { return m; },
		formatResult: formatAnimalDropdown,
		formatSelection: formatAnimalSelected
	});

	$('#procedure').select2();
});

// Automatically choose the procedure option based on previous selection
function initialSelection(procedure, animal) {
	$('#procedure').val(procedure);
	$('#animal').val(animal);
}

// Dynamically load procedures based on animal selection
$('#animal').change(function() {
	// Get new procedures
    $.post('_update-procedures', {'animal': $(this).val()}, function(data) {
        $('select[name=procedure]').find('optgroup').remove(); // Remove all existing optgroups/options
        for (var topic in data) {
            var $optgroup = $('<optgroup></optgroup>').attr('label', topic); // Add optgroup
            $('select[name=procedure]').append($optgroup);           
            for (var procedure in data[topic]) {                
                $optgroup
                    .append($('<option></option>') // Add option
                        .attr('value', data[topic][procedure])
                        .text(data[topic][procedure]));
            }
            $('select[name=procedure]').append('</optgroup>');
        }
    }, 'json');

    // Clear procedure selection
    $('#procedure').select2('val', '').removeAttr("disabled");

    // Fade out weight group
    $('#weight-control-group').fadeOut();
});

/***********************************************/
/*                Misc. Sidebar                */
/***********************************************/
// Only show weight group when a surgery and dog are selected
$('#procedure').change(function() {
	var $procedureSelect = $('select[name=procedure] option:selected'); 

	if ($procedureSelect.parent().attr('label') == 'Surgery' && $('#animal').val() == 'Dog') {
		$("#weight-control-group").fadeIn();
	}

	else {
		$("#weight-control-group").fadeOut();
	}
});
// Close banner
$('#banner-close').click(function() {
	$('#vetbanner').remove();
});

/***********************************************/
/*               Form Validation               */
/***********************************************/
// Make sure all fields are filled out
$('form').submit(function(e) {    
    // If required attribute is not supported or browser is Safari (Safari thinks that it has this attribute, but it does not work), then check all fields that has required attribute
    if (!attributeSupported('input', 'required') || isSafari()) {        
        $(this).find('[required]').each(function(index) {

            // Make sure a radio button is checked
            if ($(this).is(':radio')) {
                var name = $(this).attr('name');
                if (!$('input[name=' + name + ']:checked').length) {
                    alert("Please fill in all fields.");
                    e.preventDefault();
                    return false;
                }
            }
            // Other input types
            else if (!$(this).val()) {
                alert("Please fill in all fields.");
                e.preventDefault();
                return false;
            }
       });
    }

    // Check to make sure weight is filled out if visible (not a required field)
    var $weight = $(this).find('#weight:visible'); // Will only select weight group if it is visible
    if ($weight && $weight.val() == "") {
    	alert("Please fill in all fields.");
            e.preventDefault();
            return false;
    }

    // Also check all select fields, regardless of browser
    $(this).find('select').each(function(index) {
        if ($(this).val() == "") {
            alert("Please fill in all fields.");
            e.preventDefault();
            return false;
        }
    });
    
    return true;
});

// This checks if a specific attribute is supported (we're using the required attribute)
function attributeSupported(element, attribute) {
    return (attribute in document.createElement(element));
}

// Detect Safari (note: browser detection is bad, but detecting required attribute doesn't work for Safari)
function isSafari() {
    return (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1);
}

/***********************************************/
/*                  Feedback                   */
/***********************************************/
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