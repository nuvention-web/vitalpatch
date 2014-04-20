$("#dog_selector").change(function() {
    console.log("dog_selector changed")
    if ($(this).prop("checked")){
        $("#weight").fadeIn();
        console.log("fade in")
    }
});

$("#cat_selector").change(function() {
    console.log("cat_selector changed")
    if ($(this).prop("checked")){
        $("#weight").fadeOut();
        console.log("fade out")
    }
});