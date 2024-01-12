function logout(event) {
    let val = confirm('Do you want to logout?');

    if (val == true) {
        return true;
    } else {
        event.stopImmediatePropagation();
        event.preventDefault();
        return false;
    }
}

function myFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += " w3-theme-d1";
    } else {
        x.className = x.className.replace("w3-show", "");
        x.previousElementSibling.className =
            x.previousElementSibling.className.replace(" w3-theme-d1", "");
    }
}

// Used to toggle the menu on smaller screens when clicking on the menu button
function openNav() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}


function view_more() {

    var dots = document.getElementById("dots");
    var moreText = document.getElementById("more");
    var content = document.getElementById("content");

  
    if (dots.style.display === "none") {
      dots.style.display = "block";
      moreText.style.display = "none";
      content.innerHTML = "Read More";

    } else {
      dots.style.display = "none";
      moreText.style.display = "block";
      content.innerHTML = "Read Less";
    }
}