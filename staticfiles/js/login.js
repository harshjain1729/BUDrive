let container = document.getElementById('container1')

toggle = () => {
	container.classList.toggle('sign-in');
	container.classList.toggle('sign-up');
}


setTimeout(() => {
	container.classList.add('sign-in');
}, 200)



function show() {
    var password = document.getElementById("id_password");
    var icon = document.querySelector(".fas");

    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}

