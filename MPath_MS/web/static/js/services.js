function remove_sbml_file(sbml_file_id) {
	var data = {
		sbml_file_id: sbml_file_id,
		csrfmiddlewaretoken: csrf_token
	};
	$("#sbml_file-item-" + sbml_file_id).find("#remove-icon").html("more_horiz");
	$.post("/remove_sbml_file", data, remove_sbml_file_success.bind(null, sbml_file_id), 'json');
}

function remove_sbml_file_success(sbml_file_id, response) {
	console.log(response)
	if (response.removed) {
		$("#sbml_file-item-" + sbml_file_id).remove();
	} else {
		$("#sbml_file-item-" + sbml_file_id).find("#remove-icon").html("delete_forever");
	}
}

function generate_model(sbml_file_id) {
	var data = {
		sbml_file_id: sbml_file_id,
		csrfmiddlewaretoken: csrf_token
	};
	$("#sbml_file-item-" + sbml_file_id).find("#generate-icon").html("more_horiz");
	$.post("/generate_model", data, generate_model_success.bind(null, sbml_file_id), 'json');
}

function generate_model_success(sbml_file_id, response) {
	console.log(response);
	if (response.generated) {
		$("#sbml_file-item-" + sbml_file_id).find("a").removeClass("black-text");
		$("#sbml_file-item-" + sbml_file_id).find("#generate-icon").html("check");
	} else {
		$("#sbml_file-item-" + sbml_file_id).find("a").addClass("black-text");
		$("#sbml_file-item-" + sbml_file_id).find("#generate-icon").html("cached");
	}
}