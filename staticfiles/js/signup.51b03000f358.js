let container = document.getElementById('container1')

toggle = () => {
	container.classList.toggle('sign-in');
	container.classList.toggle('sign-up');
}


setTimeout(() => {
	container.classList.add('sign-up');
}, 200)




$('#sign_btn').on("click", function(){
	let valid = true;
	$('[required]').each(function() {
	  if ($(this).is(':invalid') || !$(this).val()) valid = false;
	})
	if (!valid) alert("error please fill all fields!");
	else alert('valid');

})

