function remove_sbml_file(sbml_file_name, csrfmiddlewaretoken) {
	var data = {
		sbml_file_name: sbml_file_name,
		csrfmiddlewaretoken: csrfmiddlewaretoken
	};
	$.post("/remove_sbml_file", data, 'json');
	$("#file-item-" + sbml_file_name).remove();
}