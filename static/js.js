

//Fade in weight text box if "dog" radio button is selected 
$("#dog_selector").change(function() {
    console.log("dog_selector changed")
    if ($(this).prop("checked")){
        $("#weight").fadeIn();
        console.log("fade in")
    }
});

//Fade out weight text box if "cat" radio button is selected.
$("#cat_selector").change(function() {
    console.log("cat_selector changed")
    if ($(this).prop("checked")){
        $("#weight").fadeOut();
        console.log("fade out")
    }
});

//Ajax function to populate the vet clinic dropdown based on zip code field.
$('#zipcode').keyup(function() {
    if($('#zipcode').val().length>=5){
      $.getJSON($SCRIPT_ROOT + '/_get_clinics_in_zipcode', {
        zipcode: $('#zipcode').val(),
      }, function(data) {

        $('#vetname_drpdwn')
            .find('option')
            .remove();

        //for each business in the yelp json response, passed here from "get_clinics_in_zipcode" function in flask:
        if(data['error']!=undefined){
            $("#zip_error").css("visibility","visible");
            console.log("fade in");
        }
        else{
            $("#zip_error").css("visibility","hidden");
            console.log("fade out");
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

