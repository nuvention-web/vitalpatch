// $( document.body ).on( 'click', '.dropdown-menu li', function( event ) {
// 	$("#procedure-form").submit();
// });

$('select.form-control').on('change', function(event) {
	$(this).parent().submit();
})