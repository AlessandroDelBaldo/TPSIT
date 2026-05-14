document.getElementById('calc-form').addEventListener('submit', function (e) {
    e.preventDefault();
    eseguiCalcolo();
});

function eseguiCalcolo() {
    var a  = document.getElementById('numA').value;
    var b  = document.getElementById('numB').value;
    var op = document.getElementById('operazione').value;

    nascondiRisultato();

    // Invia i dati al server Flask tramite XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/calcola', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Controlla il cambiamento di stato della richiesta
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            var dati = JSON.parse(xhr.responseText);
            if (xhr.status === 200 && dati.risultato !== undefined) {
                mostraRisultato(dati.risultato);
            } else {
                mostraErrore(dati.errore || 'Errore sconosciuto');
            }
        }
    };

    // Il server chiamerà il servizio SOAP e restituirà il risultato in JSON
    xhr.send(JSON.stringify({ a: a, b: b, operazione: op }));
}

function mostraRisultato(valore) {
    var box = document.getElementById('result-box');
    document.getElementById('result-value').textContent = valore;
    box.classList.remove('hidden');
    document.getElementById('error-msg').classList.add('hidden');
}

function mostraErrore(msg) {
    var err = document.getElementById('error-msg');
    err.textContent = 'Errore: ' + msg;
    err.classList.remove('hidden');
    document.getElementById('result-box').classList.add('hidden');
}

function nascondiRisultato() {
    document.getElementById('result-box').classList.add('hidden');
    document.getElementById('error-msg').classList.add('hidden');
}
