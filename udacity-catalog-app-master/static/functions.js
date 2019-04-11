$(document).ready(function() {
	$('select#categories').find('option[value="'+$('input#category_id_helper').val()+'"]').attr('selected', true);
	$('select').material_select();
});