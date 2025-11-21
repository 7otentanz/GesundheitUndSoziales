from django.shortcuts import render
from django.http import HttpResponse
import RPi.GPIO as gpio
import requests
from fpdf import FPDF

def test(request):
	return HttpResponse("Hallo.")

def einwohner(request, id):
	url = f"http://[2001:7c0:2320:2:f816:3eff:fe06:8d56]:8000/einwohner_{id}"
	response = requests.get(url)
	return render(request, "app/index.html")
	#return HttpResponse(response.text)

def geburt(request):
	if request.method == 'POST':

		#RFID-Karte auslesen und in Variable speichern
		#Berechtigungsverzeichnis auf der cbw aulesen und gucken ob ID von RFID in der Berechtigungsliste
		# if ID in Berechtigte---
		# else -> Return HttpResponse("Keine Berechtigung")

		nachname = request.POST.get("nachname_geburt")
		vorname = request.POST.get("vorname")
		geburtsdatum = request.POST.get("geburtsdatum")
		id_mutter = request.POST.get("id_mutter")
		id_vater = request.POST.get("id_vater")

#		person = {"nachname_geburt": nachname, "vorname": vorname, "geburtsdatum": geburtsdatum, "id_mutter": id_mutter, "id_vater": id_vater}
		person = {"nachname_geburt": nachname, "vorname": vorname, "geburtsdatum": geburtsdatum, "staatsangehoerigkeit": "UNSERSTAAT"}

		person_string = f"{person}"

		response = requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person)
		print(response)

#		requests.post(f"http://[2001:7c0:2320:2:f816:3eff:fe06:8d56]:8000/geburt_{person_string}/")
#		requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person)
#		requests.post("http://[2001:7c0:2320:2:f816:3eff:fe06:8d56]:8000/geburt", data=person) 
#		response.text ist die ID!

		buerger_id = response.text
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
#		pdf.output("S", "test.pdf")
		fertigespdf = pdf.output(dest="S").encode("latin-1")
		response = HttpResponse(fertigespdf, content_type="application/pdf")
		response["Content-Disposition"] = 'attachment; filename="geburtsurkunde.pdf"'

		return response

#		return HttpResponse(f"Geburt eingetragen, {response.status_code} {response.text}")



	else:
		return render(request, "app/geburt.html")
