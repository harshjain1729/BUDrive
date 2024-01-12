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
				$("#all_shared_files").load(location.href + " #all_shared_files>*", "");
            }, 4000);

        });
    };
}
