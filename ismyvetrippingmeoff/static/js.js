// Fade in weight text box if "dog" radio button is selected and a surgery is selected
function weightFadeIn() {
    var $animalRadio = $('input[name=cat_dog]:checked');
    var $procedureSelect = $('select[name=procedure] option:selected'); 

    if ($animalRadio.val() == 'dog' && $procedureSelect.parent().attr('label') == 'Surgery') {
        $('#weight').fadeIn();
    }
    else {
        $('#weight').fadeOut();
    }
}

// Bind function to change for animal radio and procedure select
$('input[name=cat_dog]').change(function() {
    weightFadeIn();
});

$('select[name=procedure]').change(function() {
    weightFadeIn();
});

var geocoder;
//Ajax function to populate the vet clinic dropdown based on zip code field.
$('#zipcode').keyup(function() {
    $("#zip_error").remove();
    console.log("fade out");
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

                    //for each business in the yelp json response, passed here from "get_clinics_in_zipcode" function in flask:
                    if(data['error']!=undefined){
                        $("#zip_error").remove();
                        $("#zip_group").append("<p id='zip_error' type='text' style='color:red;''>Sorry, that didn't work. It may be an invalid zip code. Please try a new zip code!</p>");
                        console.log("fade in");
                        $("#vetname_drpdwn").attr("disabled", "true");
                    }
                    else{
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
            alert("Geocode was not successful for the following reason: " + status);
          }
        });
    }
});

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
function gauge(percentileData) {
    // Load the Visualization API and the piechart package.
    google.load('visualization', '1.0', {'packages':['gauge']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawGauge);

    // Actually draw it!
    function drawGauge() {
        // Create and populate the data table.  Storing 0 initially so we get fun animation.
        var data = google.visualization.arrayToDataTable([
            ['Label', 'Value'],
            ['You', 0]
        ]);

        var sum = percentileData['25thPercentile'] + percentileData['median'] + percentileData['75thPercentile'];
        var borderOne = percentileData['25thPercentile'] / sum * 100;
        var borderTwo = borderOne + percentileData['median'] / sum * 100;

        var options = {
            greenFrom: 0, greenTo: borderOne,
            yellowFrom: borderOne, yellowTo: borderTwo,
            redFrom: borderTwo, redTo: 100,
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
            ['You', percentileData['userPercentile']]
        ]);
        gauge.draw(data, options);   
    }
}

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

