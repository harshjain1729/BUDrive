function addRows(emptbl, col) {
	var table = document.getElementById(emptbl);
	var rowCount = table.rows.length;
	var cellCount = table.rows[0].cells.length;
	var row = table.insertRow(rowCount);

	for (var i = 0; i <= cellCount; i++) {
		var cell = 'cell' + i;
		cell = row.insertCell(i);

		if (document.getElementById(col + i) != null) {
			var copycel = document.getElementById(col + i).innerHTML;
			cell.innerHTML = copycel;
		}

	}

}



function deleteRows(emptbl) {
	var table = document.getElementById(emptbl);
	var rowCount = table.rows.length;
	if (rowCount > '1') {
		var row = table.deleteRow(rowCount - 1);
		rowCount--;
	} else {
		alert('There should be atleast one row');
	}

}



function clears(event) {

	var record = confirm("Do you want to clear?");

	if (record == true) {
		$("#staticBackdrop").load(location.href + " #staticBackdrop>*", "");

	} else {
		event.stopImmediatePropagation();
		event.preventDefault();
		return false;
	}


}


function validateSize(input) {
	const fileSize = input.files[0].size / 1024 / 1024;
	if (fileSize > 5) {
		alert('File size exceeds 5 MB');
		input.value = "";
		return;
	}
}




function click_download(download_id) {
	document.getElementById(download_id).click();
}


function download(download_id) {
	let downloadButton = document.getElementById(download_id);

	if (downloadButton) {
		click_download(download_id);

		downloadButton.addEventListener('click', function (event) {
			event.preventDefault();

			/* Start loading process. */
			downloadButton.classList.add('loading');


			/* Set delay before switching from loading to success. */
			window.setTimeout(function () {
				downloadButton.classList.remove('loading');
				downloadButton.classList.add('success');
			}, 2000);



			/* Reset animation. */
			window.setTimeout(function () {
				downloadButton.classList.remove('success');
				$("#all_upload_files").load(location.href + " #all_upload_files>*", "");
			}, 4000);



		});
	};


}


function rename(after, before, rename) {
	document.getElementById(after).style.display = "block";
	document.getElementById(before).style.display = "none";
	document.getElementById(rename).style.display = "block";
}


function before_button(after, before, rename) {
	document.getElementById(after).style.display = "none";
	document.getElementById(before).style.display = "block";
	document.getElementById(rename).style.display = "none";

}



function submitNewFileName(event, form_id, after, before, rename) {

	if (document.getElementById(rename).style.display == "block") {
		var record = confirm("Do you want rename the file?");

		if (record == true) {
			let form = document.getElementById(form_id);
			form.submit();

		} else {
			before_button(after, before, rename);
			event.stopImmediatePropagation();
			event.preventDefault();
			return false;
		}

	}

}



function add_to_favourite(checked, file_id, csrf_token) {

	if (document.getElementById(checked).style.color == "") {
		document.getElementById(checked).style.color = "orange";

	} else {
		document.getElementById(checked).style.color = "";
	}

	$.post("", {
		star_id: file_id,
		csrfmiddlewaretoken: csrf_token
	});

}


function upload_files(form_id) {
	let form = document.getElementById(form_id);
	form.submit();
}


function delete_file(event, deleted, file_id, csrf_token) {

	var record = confirm("Do you want delete the file?");

	if (record == true) {
		document.getElementById(deleted).style.color = "red";

		$.post("", {
			trash_id: file_id,
			csrfmiddlewaretoken: csrf_token
		});

		$("#all_upload_files").load(location.href + " #all_upload_files>*", "");
		$("#all_upload_files").load(location.href + " #all_upload_files>*", "");

	} else {
		event.stopImmediatePropagation();
		event.preventDefault();
		return false;
	}

}


function share(after, before, share) {
	document.getElementById(after).style.display = "block";
	document.getElementById(before).style.display = "none";
	document.getElementById(share).style.display = "block";
}


function before_button1(after, before, share) {
	document.getElementById(after).style.display = "none";
	document.getElementById(before).style.display = "block";
	document.getElementById(share).style.display = "none";

}

function submitNewOwnerName(event, form_id, after, before, share) {

	if (document.getElementById(share).style.display == "block") {
		var record = confirm("Do you want share the file?");

		if (record == true) {
			let form = document.getElementById(form_id);
			form.submit();

		} else {
			before_button1(after, before, share);
			event.stopImmediatePropagation();
			event.preventDefault();
			return false;
		}

	}


}
