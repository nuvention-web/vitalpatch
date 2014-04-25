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

//Ajax function to populate the vet clinic dropdown based on zip code field.
$('#zipcode').keyup(function() {
    $("#zip_error").remove();
    console.log("fade out");
    if($('#zipcode').val().length>=5){
      $.getJSON($SCRIPT_ROOT + '/_get_clinics_in_zipcode', {
        zipcode: $('#zipcode').val(),
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
    }
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

