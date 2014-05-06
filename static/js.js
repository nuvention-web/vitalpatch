// Make buttons active
$('.animal button').click(function() {
    $('.animal button').removeClass('active');
    $(this).addClass('active');
});

// Fade in weight text box if "dog" radio button is selected and a surgery is selected
function weightFadeIn() {
    var $animalRadio = $('input[name=animal]:checked');
    var $procedureSelect = $('select[name=procedure] option:selected'); 

    if ($animalRadio.val() == 'dog' && $procedureSelect.parent().attr('label') == 'Surgery') {
        $('#weight input').prop('required', true);  // Make it required when visible
        $('#weight').fadeIn();
    }
    else {
        $('#weight input').prop('required', false); // Remove requirement when invisible
        $('#weight').fadeOut();
    }
}

// Fade out weight and remove required property
function weightFadeOut() {
    $('#weight input').prop('required', false); // Remove requirement when invisible
    $('#weight').fadeOut();
}

// Send an AJAX call to update the procedures dropdown based on the animal that's chosen
function updateProcedures() {
    var animal = $('input[name=animal]:checked').val();
    $.post('_update-procedures', {'animal': $('input[name=animal]:checked').val()}, function(data) {
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
}

// Bind weight and procedure functions to change for animal radio
$('input[name=animal]').change(function() {
    updateProcedures();
    weightFadeOut(); // Always fade out weight when animal button changes
});

// Bind weight function to change for procedure select
$('select[name=procedure]').change(function() {
    weightFadeIn();
});

var geocoder;
//Ajax function to populate the vet clinic dropdown based on zip code field.
$('#zipcode').keyup(function() {
    if($('#zipcode').val().length>=5){
        //Here I will use google's javascript geocoder API to get the latlng of the given zipcode, and then I will send that to the server via AJAX
        geocoder = new google.maps.Geocoder();
        geocoder.geocode( { 'address':$('#zipcode').val(), 'componentRestrictions':{'postalCode':$('#zipcode').val()} }, function(results, status) {
        
        if (status == google.maps.GeocoderStatus.OK) {
            result_latitude = results[0]['geometry']['location'].lat();
            result_longitude = results[0]['geometry']['location'].lng();
            console.log("First result latitude is: " + results[0]['geometry']['location'].lat());
            console.log("First result longitude is: " + results[0]['geometry']['location'].lng());
            //AJAX call:
            $.getJSON($SCRIPT_ROOT + '/_get_clinics_in_zipcode', {
                latitude: result_latitude,
                longitude: result_longitude
                }, function(data) {
                    $('#vetname_drpdwn')
                        .find('option')
                        .remove();
                    $('#vetname_drpdwn').append("<option value=\"\">-- Select Clinic / Animal Hospital --</option>");

                    //for each business in the yelp json response, passed here from "get_clinics_in_zipcode" function in flask:
                    if(data['error']!=undefined){
                        //If Yelp returns an error message, tell the user that something went wrong, and the zip code may be invalid
                        console.log("Yelp API returned an error");
                        showZipError("Sorry, that didn't work. It may be an invalid zip code. Please try a new zip code!");
                    }
                    else{
                        $("#zip-error").remove();
                        for (i=0; i<data['businesses'].length; i++){
                            $("#vetname_drpdwn")
                                .append($("<option></option>")
                                .attr("value", data['businesses'][i]['id'])
                                .text(data['businesses'][i]['name']))
                                .removeAttr("disabled");
                        }
                    }
            });
            return false;

          } else { //status of google.maps.GeocoderStatus is not OK
                //Show bad zip code error message
                console.log("googlemaps.GeocoderStatus is not OK");
                showZipError("Sorry, that didn't work. It may be an invalid zip code. Please try a new zip code!");                
          }
        });
    }

    // Zip code not equal to 5 characters
    else {
        showZipError("Zip codes need to be five characters!");
    }
});

// Show the error message for zip code if it's not showing or if it's different text
function showZipError(error) {
    if (!$("#zip-error").length || $("#zip-error").text() != error) {
        $("#zip-error").remove();
        $("#zip_group").append("<p id='zip-error' type='text'>" + error + "</p>");
        $('#vetname_drpdwn')
                .find('option')
                .remove();
        $('#vetname_drpdwn').append("<option value=''>-- Select Clinic / Animal Hospital --</option>");
        $("#vetname_drpdwn").attr("disabled", "true");
    }
}

// Make sure all fields are filled out
$('form').submit(function(e) {    
    // If required attribute is not supported or browser is Safari (Safari thinks that it has this attribute, but it does not work), then check all fields that has required attribute
    if (!attributeSupported('input', 'required') || isSafari()) {        
        $('form [required]').each(function(index) {

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

$('document').ready(function(){
    $('#emailSubmitButton').click(function(){
        $.getJSON($SCRIPT_ROOT + '/_submit_email', {
        email: $('#email_address_input').val(),
        }, function(data) {
            $('#email_address_input').val('');
            $("#signup_confirmation").remove();
            $("#email_group").append("<p id='signup_confirmation' style='color:green;'>Thanks for signing up! We'll be in touch :)</p> ");
        });
        return false;
    })
    $('#email_address_input').keypress(function(e){
        if(e.which == 13){  //Enter key pressed
            $('#emailSubmitButton').click();    //Trigger search button click event
        }
    });

});

// Guage
function gauge(percentile) {
    // Load the Visualization API and the piechart package.
    google.load('visualization', '1.0', {'packages':['gauge']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawGauge);

    // Actually draw it!
    function drawGauge() {
        // Create and populate the data table.  Storing 0 initially so we get fun animation.
        var data = google.visualization.arrayToDataTable([
            ['Label', 'Value'],
            ['%', 0]
        ]);

        var options = {
            greenFrom: 0, greenTo: 33,
            yellowFrom: 33, yellowTo: 67,
            redFrom: 67, redTo: 100,
            minorTicks: 5,
            animation:{
                duration: 1000,
                easing: 'out',
            }
        };

        // Create and draw the visualization.
        var gauge = new google.visualization.Gauge($('#gauge')[0]);
        gauge.draw(data, options);

        // Populate data with real value, redraw gauge.
        data = google.visualization.arrayToDataTable([
            ['Label', 'Value'],
            ['%', parseInt(percentile)]
        ]);
        gauge.draw(data, options);   
    }
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

//This code does an action when typing stops for "delay" number of milliseconds. Not used.
/*
$('#zipcode').typing({
    start: function (event, $elem) {
        //do nothing
    },
    stop: function (event, $elem) {
        $.getJSON($SCRIPT_ROOT + '/_get_clinics_in_zipcode', {
            zipcode: $('#zipcode').val(),
        }, function(data) {
            //delete all option in the clinic-select dropdown
            $('#vetname_drpdwn')
                .find('option')
                .remove();

            //for each business in the yelp json response, passed here from "get_clinics_in_zipcode" function in flask, add an option to the select
            for (i=0; i<data['businesses'].length; i++){
                $("#vetname_drpdwn")
                    .append($("<option></option>")
                    .attr("value", data['businesses'][i]['id'])
                    .text(data['businesses'][i]['name']));
            }
        });
        return false;
    },
    delay: 300
});
*/

