function search(e) {
    e.preventDefault();
    var form = document.getElementById("form");
    var formData = new FormData(form);
    var text = formData.get("code");
    if (!text.match(/[A-Z][0-9]{3}/)) {
        document.getElementById("results").innerHTML = "";
        alert("Formato non valido. Es. A001");
    } else {
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (request.readyState == XMLHttpRequest.OPENED) {
                document.getElementById("results").innerHTML = '';
            } else if (request.readyState == XMLHttpRequest.DONE && request.status == 200) {
                document.getElementById("results").innerHTML = request.responseText;
            }
        }
        request.open("GET", "/?code-" + text);
        request.send();
    }
    return false;
}
