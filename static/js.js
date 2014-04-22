

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
$(function() {
    $('#zipcode').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_get_clinics_in_zipcode', {
        zipcode: $('#zipcode').val(),
      }, function(data) {
        $('#vetname_drpdwn')
            .find('option')
            .remove();

        //for each business in the yelp json response, passed here from "get_clinics_in_zipcode" function in flask:
        for (i=0; i<data['businesses'].length; i++){
            $("#vetname_drpdwn")
                .append($("<option></option>")
                .attr("value", data['businesses'][i]['id'])
                .text(data['businesses'][i]['name']));
        }
      });
      return false;
    });
});


/*
//setup before functions
var typingTimer;                //timer identifier
var doneTypingInterval = 1000;  //time in ms, 5 second for example

//on keyup, start the countdown
$('#zipcode').keyup(function(){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
    console.log("keyup");
});

//on keydown, clear the countdown 
$('#zipcode').keydown(function(){
    clearTimeout(typingTimer);
    console.log("keydown");
});

//Ajax function to populate the vet clinic dropdown based on zip code field.
function doneTyping() {
    $('#zipcode').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_get_clinics_in_zipcode', {
        zipcode: $('#zipcode').val(),
      }, function(data) {
        $('#vetname_drpdwn')
            .find('option')
            .remove();

        //for each business in the yelp json response, passed here from "get_clinics_in_zipcode" function in flask:
        for (i=0; i<data['businesses'].length; i++){
            $("#vetname_drpdwn")
                .append($("<option></option>")
                .attr("value", data['businesses'][i]['id'])
                .text(data['businesses'][i]['name']));
        }
      });
      return false;
    });
}

*/