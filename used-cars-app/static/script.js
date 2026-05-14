// Intercetta il submit della form e avvia la ricerca AJAX
document.getElementById('search-form').addEventListener('submit', function (e) {
    e.preventDefault();
    cercaAuto();
});

// Invia la richiesta al server tramite XMLHttpRequest
function cercaAuto() {
    var brand    = document.getElementById('brand').value;
    var model    = document.getElementById('model').value;
    var fuelType = document.getElementById('fuel_type').value;
    var color    = document.getElementById('color').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/cars', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Callback che viene eseguita ad ogni cambiamento di stato della richiesta
    xhr.onreadystatechange = function () {
        // Stato DONE (4): la risposta è arrivata completamente
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var cars = JSON.parse(xhr.responseText);
                mostraRisultati(cars);
            } else {
                document.getElementById('cars-tbody').innerHTML =
                    '<tr><td colspan="5" class="no-results">Errore nella comunicazione col server.</td></tr>';
            }
        }
    };

    // Invia i dati della form codificati in JSON
    xhr.send(JSON.stringify({
        brand:     brand,
        model:     model,
        fuel_type: fuelType,
        color:     color
    }));
}

// Aggiorna la tabella HTML con i risultati ricevuti dal server
function mostraRisultati(cars) {
    var tbody = document.getElementById('cars-tbody');
    var count = document.getElementById('results-count');
    tbody.innerHTML = '';

    if (cars.length === 0) {
        count.textContent = 'Nessun risultato trovato.';
        tbody.innerHTML =
            '<tr><td colspan="5" class="no-results">Nessuna auto corrisponde ai criteri di ricerca.</td></tr>';
        return;
    }

    count.textContent = cars.length + ' auto trovate';

    // Crea una riga per ogni automobile filtrata
    cars.forEach(function (car) {
        var tr = document.createElement('tr');
        tr.innerHTML =
            '<td><img src="' + car.image_url + '" alt="' + car.brand + ' ' + car.model + '"></td>' +
            '<td><strong>' + car.brand + '</strong></td>' +
            '<td>' + car.model + '</td>' +
            '<td><span class="fuel-badge">' + car.fuel_type + '</span></td>' +
            '<td><span class="color-badge">' + car.color + '</span></td>';
        tbody.appendChild(tr);
    });
}

// All'avvio della pagina carica tutte le auto disponibili
window.addEventListener('load', function () {
    cercaAuto();
});
