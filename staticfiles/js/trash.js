function delete_file(event, file_id, csrf_token) {


	var record = confirm("Do you want permanently delete the file?");

	if (record == true) {
		$.post("", {
			delete_id: file_id,
			csrfmiddlewaretoken: csrf_token
		});

		$("#all_deleted_files").load(location.href + " #all_deleted_files>*", "");
		$("#all_deleted_files").load(location.href + " #all_deleted_files>*", "");

	} else {
		event.stopImmediatePropagation();
		event.preventDefault();
		return false;
	}
}


function restore_file(event, file_id, csrf_token) {

	var record = confirm("Do you want restore the file?");

	if (record == true) {
		$.post("", {
			restore_id: file_id,
			csrfmiddlewaretoken: csrf_token
		});

		$("#all_deleted_files").load(location.href + " #all_deleted_files>*", "");
		$("#all_deleted_files").load(location.href + " #all_deleted_files>*", "");

	} else {
		event.stopImmediatePropagation();
		event.preventDefault();
		return false;
	}
}
