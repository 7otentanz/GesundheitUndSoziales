from django.shortcuts import render
from django.http import HttpResponse
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
#from fpdf import FPDF

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
		print(f"Personenregister: {neugeboren}")

		buerger_id = neugeboren.text
		id_kind = {"id_kind": buerger_id}

		kindergeld = requests.post("http://[2001:7c0:2320:2:f816:3eff:fed4:e456]:1810/kindergeldanlegen", data=id_kind)
		print(f"Kindergeld: {kindergeld}")

		elterngeldanlegen = requests.post("http://[2001:7c0:2320:2:f816:3eff:fed4:e456]:1810/elterngeldanlegen", data=elterngeld)
		print(f"Elterngeld: {elterngeldanlegen}")

		# Zurückgegebene Bürger ID auf RFID Karte schreiben
		reader = SimpleMFRC522()
		reader.write(buerger_id)
		print(f"RFID-Karte beschrieben mit {buerger_id}.")

		return HttpResponse(f"Herzlichen Glückwunsch zur Geburt von {vorname}.")

	else:
		return render(request, "app/geburt.html")

def tod(request):
	if request.method == 'POST':

		sterbedatum = request.POST.get("sterbedatum")

		# Bürger ID aus RFID Karte auslesen
		reader = SimpleMFRC522()
		id, data = reader.read()
		id_person = data

		person = {"buerger_id": id_person, "sterbedatum": sterbedatum}

		response = requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person)
		print(response)

		return HttpResponse(f"{id_person} ist verstorben am {sterbedatum}. Requiescat in pace.")

	else:
		return render(request, "app/tod.html")