$('select.form-control').on('change', function(event) {
	$(this).parent().submit();
})