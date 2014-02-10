var seeking = false;

// Check if device is mobile
window.mobilecheck = function() {
	var check = false;
	(function(a) {
		if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))
			check = true})(navigator.userAgent||navigator.vendor||window.opera);
	return check; 
}

// Onload
$(document).ready(function() {

	// if (!window.mobilecheck()) {
	// 	$("body").append("<p>Sorry, you must be on a mobile device to access SEEK.</p>");
	// 	return;
	// }

	// Check if you're the first person there
	$("body").append("<p class=\"waiting\">Waiting for other player...</p>");
	getLocation();
});

// Let's Go!
$("button").click(function() {
	seeking = true;
	$(this).fadeOut();
});

// Make sure you tell the other person to stop looking for you
$(window).unload(function() {
	$.ajax({
		type: "POST",
		url:  "/location",
		data: { isHere: false }
	});
});

// POSITION
// Get the current location of the user
function getLocation() {
	if (navigator.geolocation) {		
	    navigator.geolocation.getCurrentPosition(positionSuccess, positionError);
    }
	else {
		$("body").append("<p>Geolocation is not supported by this browser.<p>");
	}
	window.setTimeout(getLocation, 5000);
} 
// If the position is successful
function positionSuccess(position) {
	$("body").append("<p>Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude + "</p>");

	$.ajax({
		type: "POST",
		url:  "/location",
		data: { isHere: true, latitude: position.coords.latitude, longitude: position.coords.longitude }
	}).done(function(otherCoords) {
    	if (otherCoords.isHere) {
    		// Change waiting message to button
    		if ($("p.waiting").length > 0) {
	    		$("p.waiting").fadeOut("slow", function() {
					$(".button-wrapper").fadeIn("slow");
					$("p.waiting").remove();
				});
	    	}

	    	// If they pressed the button
	    	if (seeking) {
				// Calculate distance
				var R = 6371; // km
				var dLat = (otherCoords.latitude-position.latitude).toRad();
				var dLon = (otherCoords.longitude-position.longitude).toRad();
				var lat1 = position.latitude.toRad();
				var lat2 = otherCoords.latitude.toRad();
				var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
				        Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
				var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
				var d = R * c;
				console.log(d);

				// No divide-by-zero errors
				if (d < 0) 
					d = 1;

				// Change background color
				if (d > 100)
					$("body").css("background-color", "rgb(0, 0, 255)");
				else
					$("body").css("background-color", "rgb(" + String(255/d) + ", 0," + String(255 - 255/d) + ")");	
			}
    	}
    	else if (otherCoords.isHere != null) {
    		// Other user signed off
    		$("body").html("<p>The other player stopped seeking you :(</p>");
    	}
  	});
}
// If there's an error
function positionError(error) {
	$("body").append("<p>ERROR: " + error.message + "</p>");
}

