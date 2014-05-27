/***********************************************/
/*                    Gauge                    */
/***********************************************/
var gauge;
var nationalPercentile;
var urbanPercentile;
var suburbanPercentile;
var ruralPercentile;
var options; // Graph options
var choice;  // Current area wealth choice

function gauge(percentileData) {
    // Load the Visualization API and the piechart package
    google.load('visualization', '1.0', {'packages':['gauge']});

    // Set a callback to run when the Google Visualization API is loaded
    google.setOnLoadCallback(drawGauge);

    // Actually draw it!
    function drawGauge() {
        // Create and populate the data table.  Storing 0 initially so we get fun animation
        data = google.visualization.arrayToDataTable([
            ['Label', 'Value'],
            ['%', 0]
        ]);

        options = {
            height: 175,
            width: 175,
            greenFrom: 0, greenTo: 33,
            yellowFrom: 33, yellowTo: 67,
            redFrom: 67, redTo: 100,
            minorTicks: 5,
            animation:{
                duration: 1000,
                easing: 'out',
            }
        };

        // Create and draw the visualization
        gauge = new google.visualization.Gauge($('#gauge')[0]);
        gauge.draw(data, options);

        // Populate data with real values, redraw gauge
        nationalPercentile = parseInt(percentileData.national);
        urbanPercentile    = parseInt(percentileData.urban);
        suburbanPercentile = parseInt(percentileData.suburban);
        ruralPercentile    = parseInt(percentileData.rural);

        if (choice === undefined) {
            choice = 0;            
        }          

        // In case someone clicks a button before the gauge loads
        updateGauge();
    }
}

function updateGauge() {
    var percentile;

    switch(choice) {
    case 1:
        percentile = urbanPercentile;
        areaText = 'in urban areas'
        break;
    case 2:
        percentile = suburbanPercentile;
        areaText = 'in suburban areas'
        break;
    case 3:
        percentile = ruralPercentile;
        areaText = 'in rural areas'
        break;
    default:
        percentile = nationalPercentile;
        areaText = 'nationwide'
        break;
    }

    // Gauge
    data = google.visualization.arrayToDataTable([
            ['Label', 'Value'],
            ['%', parseInt(percentile)]
    ]);
    gauge.draw(data, options);

    // Set text below gauge
    $('#gauge-percentile').text(percentile + '%');
    $('#gauge-area').text(areaText);
}

// Change active state of buttons, update gauge
$('.area-button').click(function() {
    $('.area-button').removeClass('active');
    $(this).addClass('active');

    choice = $(this).index();

    // Update gauge
    updateGauge();
});

/***********************************************/
/*               Email Collection              */
/***********************************************/
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