from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Riferimento al servizio SOAP originale (attualmente offline):
# SOAP_URL = 'http://www.dneonline.com/calculator.asmx'
#
# La busta SOAP che verrebbe inviata al servizio aveva questa forma:
#
# <?xml version="1.0" encoding="utf-8"?>
# <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap:Body>
#     <Add xmlns="http://tempuri.org/">
#       <intA>5</intA>
#       <intB>3</intB>
#     </Add>
#   </soap:Body>
# </soap:Envelope>
#
# E la risposta XML conteneva: <AddResult>8</AddResult>


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calcola', methods=['POST'])
def calcola():
    data = request.json
    op = data.get('operazione', '')
    a  = data.get('a', 0)
    b  = data.get('b', 0)

    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return jsonify({'errore': 'Operandi non validi'}), 400

    # Implementazione locale delle operazioni (equivalente al servizio SOAP)
    if op == 'Add':
        risultato = a + b
    elif op == 'Subtract':
        risultato = a - b
    elif op == 'Multiply':
        risultato = a * b
    elif op == 'Divide':
        if b == 0:
            return jsonify({'errore': 'Divisione per zero non consentita'}), 400
        risultato = a / b
    else:
        return jsonify({'errore': 'Operazione non valida'}), 400

    # Restituisce intero se il risultato non ha decimali
    if risultato == int(risultato):
        risultato = int(risultato)

    return jsonify({'risultato': risultato})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
