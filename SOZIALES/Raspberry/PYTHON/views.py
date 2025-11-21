from django.shortcuts import render
from django.http import HttpResponse
import RPi.GPIO as gpio
import requests
from fpdf import FPDF

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