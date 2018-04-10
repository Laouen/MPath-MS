function remove_sbml_file(sbml_file_id) {
	var data = {
		sbml_file_id: sbml_file_id,
		csrfmiddlewaretoken: csrf_token
	};
	$.post("/remove_sbml_file", data, function(d) { console.log(d); }, 'json');
	$("#sbml_file-item-" + sbml_file_id).remove();
}