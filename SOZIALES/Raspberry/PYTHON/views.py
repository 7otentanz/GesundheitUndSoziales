from django.shortcuts import render,redirect
from django.http import HttpResponse
import RPi.GPIO as gpio
import requests
from fpdf import FPDF
from project.jwt_tooling import decode_jwt


static = "/var/www/static"

def jwt_login(request):
    token = request.GET.get("token")
    if not token:
        return HttpResponse("Kein Token übergeben.", status=400)

    try:
        daten = decode_jwt(token)
    except Exception:
        return HttpResponse("Ungültiges oder abgelaufenes Token.", status=401)

    buerger_id = daten.get("user_id")
    if not buerger_id:
        return HttpResponse("Token enthält keine buerger_id.", status=400)

    # Session auf Server B setzen
    request.session["user_id"] = buerger_id

    # Weiter ins Dashboard
    return redirect("immigration") #hier anpassen, weiterleiten auf die Zielseite

def immigration(request):
	if request.method == 'POST':

		nachname = request.POST.get("nachname")
		vorname = request.POST.get("vorname")
		geburtsdatum = request.POST.get("geburtsdatum")
		

		person = {"nachname": nachname, "vorname": vorname, "geburtsdatum": geburtsdatum, "staatsangehoerigkeit": "UNSERSTAAT"}

		response = requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person)
		#URL anpassen
		print(response)

		buerger_id = response.text
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font("Arial", style="B", size=16)
		pdf.cell(0, 20, "Einbürgerungsurkunde", align="C", ln=True)
		pdf.ln(20)
		pdf.set_font("Arial", size=14)
		pdf.cell(20, 0, f"Nachname: {nachname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Vorname: {vorname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Buerger ID: {buerger_id}") 

		fertigespdf = pdf.output(dest="S").encode("latin-1")
		response = HttpResponse(fertigespdf, content_type="application/pdf")
		response["Content-Disposition"] = "attachment; filename='immigrationsurkunde.pdf'"

		return response

	else:
		return render(request, "app/immigration.html")


def emigration(request):
	if request.method == 'POST':

		id_person = request.POST.get("id_person")
		emigration = request.POST.get("emigrationsdatum")

		person = {"buerger_id": id_person, "emigration": emigration}

		response = requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person)
		# hier noch richtige URL eintragen
		print(response)

		vorname = "Vorname"
		#vorname = requests.get(URL/{id})
		nachname = "Nachname"
		#samesame

		pdf = FPDF()
		pdf.add_page()
		pdf.set_font("Arial", style="B", size=16)
		pdf.cell(0, 20, "Emigrationsurkunde", align="C", ln=True)
		pdf.ln(20)
		pdf.set_font("Arial", size=14)
		pdf.cell(20, 0, f"Nachname: {nachname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Vorname: {vorname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Emigrationsdatum: {emigration}") 

		fertigespdf = pdf.output(dest="S").encode("latin-1")
		response = HttpResponse(fertigespdf, content_type="application/pdf")
		response["Content-Disposition"] = "attachment; filename='emigrationsurkunde.pdf'"

		return response
	
	else:
		return render(request, "app/emigration.html")
	

def sozialleistungen(request):
	buerger_id = request.session.get("user_id")

	api = f"http://[2001:7c0:2320:2:f816:3eff:fed4:e456]:1810/api_sozialleistungen/{buerger_id}"

	response = requests.get(api)
	daten = response.json()
	return render(request, "sozialleistungen.html", {"user_id" : buerger_id, "daten" : daten})
