// Espressioni regolari per validazione lato client
var regexNome = /^[A-Za-zÀ-ÿ\s]{2,50}$/;
var regexData = /^\d{4}-\d{2}-\d{2}$/;
var regexMansione = /^[A-Za-zÀ-ÿ\s]{2,100}$/;

function ajax(method, url, data, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      var risposta = null;
      try { risposta = JSON.parse(xhr.responseText); } catch (e) {}
      callback(xhr.status, risposta);
    }
  };
  xhr.send(data ? JSON.stringify(data) : null);
}

function validaUtente(nome, cognome, data, mansione, divErrori) {
  var errori = [];
  if (!regexNome.test(nome.trim())) errori.push('Nome non valido (solo lettere, 2-50 caratteri)');
  if (!regexNome.test(cognome.trim())) errori.push('Cognome non valido (solo lettere, 2-50 caratteri)');
  if (!regexData.test(data)) errori.push('Data di nascita non valida (formato YYYY-MM-DD)');
  if (!regexMansione.test(mansione.trim())) errori.push('Mansione non valida (solo lettere, 2-100 caratteri)');

  divErrori.innerHTML = '';
  if (errori.length > 0) {
    divErrori.innerHTML = '<ul><li>' + errori.join('</li><li>') + '</li></ul>';
    return false;
  }
  return true;
}

function caricaUtenti() {
  ajax('GET', '/gestionale_utenti/users/', null, function (status, data) {
    var tbody = document.getElementById('corpo-tabella');
    var msg = document.getElementById('messaggio-lista');
    msg.innerHTML = '';
    if (status !== 200 || !data) {
      tbody.innerHTML = '<tr><td colspan="6">Errore nel caricamento degli utenti.</td></tr>';
      return;
    }
    if (data.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6">Nessun utente presente.</td></tr>';
      return;
    }
    var html = '';
    for (var i = 0; i < data.length; i++) {
      var u = data[i];
      html += '<tr>';
      html += '<td>' + u.id + '</td>';
      html += '<td>' + u.nome + '</td>';
      html += '<td>' + u.cognome + '</td>';
      html += '<td>' + u.data_nascita + '</td>';
      html += '<td>' + u.mansione + '</td>';
      html += '<td>';
      html += '<button onclick="mostraDettaglio(' + u.id + ')">Dettaglio</button> ';
      html += '<button onclick="mostraModifica(' + u.id + ', \'' + u.nome + '\', \'' + u.cognome + '\', \'' + u.data_nascita + '\', \'' + u.mansione + '\')">Modifica</button> ';
      html += '<button class="btn-elimina" onclick="eliminaUtente(' + u.id + ')">Elimina</button>';
      html += '</td>';
      html += '</tr>';
    }
    tbody.innerHTML = html;
  });
}

function mostraDettaglio(id) {
  ajax('GET', '/gestionale_utenti/users/' + id, null, function (status, data) {
    var sezione = document.getElementById('sezione-dettaglio');
    var contenuto = document.getElementById('dettaglio-contenuto');
    if (status === 200 && data) {
      contenuto.innerHTML =
        '<p><strong>ID:</strong> ' + data.id + '</p>' +
        '<p><strong>Nome:</strong> ' + data.nome + '</p>' +
        '<p><strong>Cognome:</strong> ' + data.cognome + '</p>' +
        '<p><strong>Data di nascita:</strong> ' + data.data_nascita + '</p>' +
        '<p><strong>Mansione:</strong> ' + data.mansione + '</p>';
      sezione.style.display = 'block';
      sezione.scrollIntoView({ behavior: 'smooth' });
    } else if (status === 404) {
      alert('Utente non trovato.');
    } else {
      alert('Errore nel caricamento del dettaglio.');
    }
  });
}

function nascondiDettaglio() {
  document.getElementById('sezione-dettaglio').style.display = 'none';
}

function inserisciUtente(event) {
  event.preventDefault();
  var nome = document.getElementById('ins-nome').value;
  var cognome = document.getElementById('ins-cognome').value;
  var data = document.getElementById('ins-data').value;
  var mansione = document.getElementById('ins-mansione').value;
  var divErrori = document.getElementById('errori-inserimento');
  var msg = document.getElementById('messaggio-inserimento');

  if (!validaUtente(nome, cognome, data, mansione, divErrori)) return;

  var payload = { nome: nome.trim(), cognome: cognome.trim(), data_nascita: data, mansione: mansione.trim() };
  ajax('POST', '/gestionale_utenti/users/', payload, function (status, risposta) {
    msg.innerHTML = '';
    divErrori.innerHTML = '';
    if (status === 201) {
      msg.innerHTML = '<p class="successo">Utente inserito con ID ' + risposta.id + '.</p>';
      document.getElementById('form-inserimento').reset();
      caricaUtenti();
    } else if (status === 400 && risposta && risposta.errors) {
      divErrori.innerHTML = '<ul><li>' + risposta.errors.join('</li><li>') + '</li></ul>';
    } else {
      msg.innerHTML = '<p class="errore">Errore durante l\'inserimento.</p>';
    }
  });
}

function mostraModifica(id, nome, cognome, data, mansione) {
  document.getElementById('mod-id').value = id;
  document.getElementById('mod-nome').value = nome;
  document.getElementById('mod-cognome').value = cognome;
  document.getElementById('mod-data').value = data;
  document.getElementById('mod-mansione').value = mansione;
  document.getElementById('modifica-id-titolo').textContent = '(ID: ' + id + ')';
  document.getElementById('errori-modifica').innerHTML = '';
  document.getElementById('messaggio-modifica').innerHTML = '';
  var sezione = document.getElementById('sezione-modifica');
  sezione.style.display = 'block';
  sezione.scrollIntoView({ behavior: 'smooth' });
}

function nascondiModifica() {
  document.getElementById('sezione-modifica').style.display = 'none';
}

function modificaUtente(event) {
  event.preventDefault();
  var id = document.getElementById('mod-id').value;
  var nome = document.getElementById('mod-nome').value;
  var cognome = document.getElementById('mod-cognome').value;
  var data = document.getElementById('mod-data').value;
  var mansione = document.getElementById('mod-mansione').value;
  var divErrori = document.getElementById('errori-modifica');
  var msg = document.getElementById('messaggio-modifica');

  if (!validaUtente(nome, cognome, data, mansione, divErrori)) return;

  var payload = { nome: nome.trim(), cognome: cognome.trim(), data_nascita: data, mansione: mansione.trim() };
  ajax('PUT', '/gestionale_utenti/users/' + id, payload, function (status, risposta) {
    msg.innerHTML = '';
    divErrori.innerHTML = '';
    if (status === 200) {
      msg.innerHTML = '<p class="successo">Utente modificato con successo.</p>';
      caricaUtenti();
    } else if (status === 404) {
      msg.innerHTML = '<p class="errore">Utente non trovato.</p>';
    } else if (status === 400 && risposta && risposta.errors) {
      divErrori.innerHTML = '<ul><li>' + risposta.errors.join('</li><li>') + '</li></ul>';
    } else {
      msg.innerHTML = '<p class="errore">Errore durante la modifica.</p>';
    }
  });
}

function eliminaUtente(id) {
  if (!confirm('Eliminare l\'utente con ID ' + id + '?')) return;
  ajax('DELETE', '/gestionale_utenti/users/' + id, null, function (status, risposta) {
    if (status === 200) {
      caricaUtenti();
    } else if (status === 404) {
      alert('Utente non trovato.');
    } else {
      alert('Errore durante l\'eliminazione.');
    }
  });
}

// Carica la lista all'avvio
window.onload = function () {
  caricaUtenti();
};
