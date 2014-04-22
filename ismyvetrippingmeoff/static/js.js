

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

//Set hidden field's value to the *name* of the vet clinic that has been selected in the vetname_drpdwn select field
$('#zipcode').on('change', function() {
  $('#vet_name').value = $("#vetname_drpdwn option:selected").text()
});


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


