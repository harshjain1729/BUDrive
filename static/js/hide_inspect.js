// take body to change the content
const body = document.getElementsByTagName('body');
// stop keyboard shortcuts
window.addEventListener("keydown", (event) => {
    if (event.ctrlKey && (event.key === "S" || event.key === "s")) {
        event.preventDefault();
        // body[0].innerHTML = "Sorry, you can't do this 💔..."
    }

    if (event.ctrlKey && (event.key === "C")) {
        event.preventDefault();
        // body[0].innerHTML = "Sorry, you can't do this 💔..."
    }
    if (event.ctrlKey && (event.key === "E" || event.key === "e")) {
        event.preventDefault();
        // body[0].innerHTML = "Sorry, you can't do this 💔..."
    }
    if (event.ctrlKey && (event.key === "I" || event.key === "i")) {
        event.preventDefault();
        // body[0].innerHTML = "Sorry, you can't do this 💔...";
    }
    if (event.ctrlKey && (event.key === "K" || event.key === "k")) {
        event.preventDefault();
        // body[0].innerHTML = "Sorry, you can't do this 💔...";
    }
    if (event.ctrlKey && (event.key === "U" || event.key === "u")) {
        event.preventDefault();
        // body[0].innerHTML = "Sorry, you can't do this 💔...";
    }
});
// stop right click
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
});


document.onkeydown = function(e) {
    if (event.keyCode == 123) {
        return false;
    }
    if (e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'C'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'X'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'Y'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'Z'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'V'.charCodeAt(0)) {
        return false;
    }
    if (e.keyCode == 67 && e.shiftKey && (e.ctrlKey || e.metaKey)) {
        return false;
    }
    if (e.keyCode == 'J'.charCodeAt(0) && e.altKey && (e.ctrlKey || e.metaKey)) {
        return false;
    }
    if (e.keyCode == 'I'.charCodeAt(0) && e.altKey && (e.ctrlKey || e.metaKey)) {
        return false;
    }
    if ((e.keyCode == 'V'.charCodeAt(0) && e.metaKey) || (e.metaKey && e.altKey)) {
        return false;
    }
    if (e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'S'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'H'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'A'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'F'.charCodeAt(0)) {
        return false;
    }
    if (e.ctrlKey && e.keyCode == 'E'.charCodeAt(0)) {
        return false;
    }
}
if (document.addEventListener) {
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    }, false);
} else {
    document.attachEvent('oncontextmenu', function() {
        window.event.returnValue = false;
    });
}
