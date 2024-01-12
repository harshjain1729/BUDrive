var btec = ["CSE", "CSAM", "CSAI", "CSSS", "CSD", "CSB", "ECE"];
var mtec = ["CSE", "ECE", "CB"];
var phd = ["CSE", "ECE", "SSH", "HCD", "CB", "MATHS"];

function programmes() {

    if (document.getElementById('programme').value != "none") {

        let prog = document.getElementById('programme').value;
        let select = document.getElementById("branch");

        if (prog == "B.Tech") {
            document.getElementById("branch").innerHTML = "";
            for (let i = 0; i < btec.length; i++) {
                let optn = btec[i];
                let el = document.createElement("option");
                el.textContent = optn;
                el.value = optn;
                select.appendChild(el);
            }

        }

        if (prog == "M.Tech") {
            document.getElementById("branch").innerHTML = "";
            for (let i = 0; i < mtec.length; i++) {
                let optn = mtec[i];
                let el = document.createElement("option");
                el.textContent = optn;
                el.value = optn;
                select.appendChild(el);
            }

        }

        if (prog == "Ph.D") {
            document.getElementById("branch").innerHTML = "";
            for (let i = 0; i < phd.length; i++) {
                let optn = phd[i];
                let el = document.createElement("option");
                el.textContent = optn;
                el.value = optn;
                select.appendChild(el);
            }

        }

    } else {
        document.getElementById("branch").innerHTML = "";

        let select = document.getElementById("branch");
        let el = document.createElement("option");
        el.textContent = "Select";
        el.value = "none";
        select.appendChild(el);
    }

}


$(document).ready(function() {
    var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }


    $(".file-upload").on('change', function(){
        readURL(this);
    });

    $(".upload-button").on('click', function() {
       $(".file-upload").click();
    });
});


function upload_photo() {
	let photo = document.getElementById('profile_image').value;

	if(photo == "") {
		alert("Select a profile photo");
		return false;
	}

	return true;
}
