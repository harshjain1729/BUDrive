function click_download(download_id) {
    document.getElementById(download_id).click();
}

function download(download_id) {
    let downloadButton = document.getElementById(download_id);
    // document.getElementById('download').click();
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
				$("#all_starred_files").load(location.href + " #all_starred_files>*", "");
            }, 4000);

        });
    };
}


function remove_from_favourite(event, file_id, csrf_token) {

	var record = confirm("Do you want unstar the file?");

	if (record == true) {
		$.post("", {
			unstar_id: file_id,
			csrfmiddlewaretoken: csrf_token
		});

		$("#all_starred_files").load(location.href + " #all_starred_files>*", "");
		$("#all_starred_files").load(location.href + " #all_starred_files>*", "");

	} else {
		event.stopImmediatePropagation();
		event.preventDefault();
		return false;
	}

}



function delete_file(event, deleted, file_id, csrf_token) {
	var record = confirm("Do you want delete the file?");

	if (record == true) {
		document.getElementById(deleted).style.color = "red";

		$.post("", {
			trash_id: file_id,
			csrfmiddlewaretoken: csrf_token
		});

		$("#all_starred_files").load(location.href + " #all_starred_files>*", "");
		$("#all_starred_files").load(location.href + " #all_starred_files>*", "");

	} else {
		event.stopImmediatePropagation();
		event.preventDefault();
		return false;
	}


}
