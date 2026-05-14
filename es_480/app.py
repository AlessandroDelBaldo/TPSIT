import os
from zeep import Client
from zeep.exceptions import Fault
from flask import Flask, request, render_template

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))

# soap service
url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"

def getAllISOCodes(client):
    return client.service.ListOfCountryNamesByCode()


@app.route("/", methods=["GET", "POST"])
def load():
    result = None
    response = None
    service_used = None
    isocode = ""
    try:
        client = Client(wsdl=url)
        if request.method == "POST":
            isocode = request.form.get("isocode", "").strip()
            service = request.form.get("service", "CapitalCity")
            if not isocode:
                result = "Inserisci un codice ISO."
            else:
                service_used = service
                if service == "CapitalCity":
                    response = client.service.CapitalCity(sCountryISOCode=isocode)
                elif service == "CountryIntPhoneCode":
                    response = client.service.CountryIntPhoneCode(sCountryISOCode=isocode)
                elif service == "FullCountryInfo":
                    response = client.service.FullCountryInfo(sCountryISOCode=isocode)
                else:
                    result = "Servizio non valido."
            return render_template("home.html.jinja", response=response,
                                   result=result, service_used=service_used,
                                   isocode=isocode)
        else:
            countries = getAllISOCodes(client)
            return render_template("home.html.jinja", countries=countries)
    except Fault as exception:
        return f"Errore SOAP: {exception}"

# pip install zeep
# rif. https://docs.python-zeep.org/en/master/
if __name__ == "__main__":
    app.run(debug=True)
