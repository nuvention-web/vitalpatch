$('select.form-control').on('change', function(event) {
	$(this).parent().submit();
})

$(document).ready(function() {
	$('form').delay(500).animate({'left': '50%', 'margin-left': -$('form').width()/2 });
});