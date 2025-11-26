from django.shortcuts import render
from django.http import HttpResponse
import RPi.GPIO as gpio
import requests
from fpdf import FPDF

def geburt(request):
	if request.method == 'POST':

		nachname = request.POST.get("nachname_geburt")
		vorname = request.POST.get("vorname")
		geburtsdatum = request.POST.get("geburtsdatum")
		id_mutter = request.POST.get("id_mutter")
		id_vater = request.POST.get("id_vater")

		person = {"nachname_geburt": nachname, "vorname": vorname, "geburtsdatum": geburtsdatum, "staatsangehoerigkeit": "UNSERSTAAT"}
		elterngeld = {"id_vater": id_vater, "id_mutter": id_mutter}

		neugeboren = requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person)
		print(neugeboren)

		elterngeldanlegen = requests.post("http://[2001:7c0:2320:2:f816:3eff:fed4:e456]:1810/elterngeldanlegen", data=elterngeld)
		print(elterngeldanlegen)

		buerger_id = neugeboren.text
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font("Arial", style="B", size=16)
		pdf.cell(0, 20, "Geburtsurkunde", align="C", ln=True)
		pdf.ln(20)
		pdf.set_font("Arial", size=14)
		pdf.cell(20, 0, f"Geburtsname: {nachname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Vorname: {vorname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Buerger ID: {buerger_id}") 

		fertigespdf = pdf.output(dest="S").encode("latin-1")
		response = HttpResponse(fertigespdf, content_type="application/pdf")
		response["Content-Disposition"] = "attachment; filename=geburtsurkunde.pdf"

		return response

	else:
		return render(request, "app/geburt.html")

def tod(request):
	if request.method == 'POST':

		id_person = request.POST.get("id_person")
		sterbedatum = request.POST.get("sterbedatum")

		person = {"buerger_id": id_person, "sterbedatum": sterbedatum}

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
		pdf.cell(0, 20, "Sterbeurkunde", align="C", ln=True)
		pdf.ln(20)
		pdf.set_font("Arial", size=14)
		pdf.cell(20, 0, f"Nachname: {nachname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Vorname: {vorname}")
		pdf.ln(5)
		pdf.cell(20, 0, f"Sterbedatum: {sterbedatum}") 

		fertigespdf = pdf.output(dest="S").encode("latin-1")
		response = HttpResponse(fertigespdf, content_type="application/pdf")
		response["Content-Disposition"] = "attachment; filename='sterbeurkunde.pdf'"

		return response
	
	else:
		return render(request, "app/tod.html")
