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

    // Also check all select fields, regardless of browser
    $(this).find('select').each(function(index) {
        if ($(this).val() == "" || $(this).prop('disabled')) {
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