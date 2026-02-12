from django.shortcuts import render, redirect
from django.http import HttpResponse
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time
from project.jwt_tooling import decode_jwt
#from fpdf import FPDF

def jwt_login(request):
    token = request.GET.get("token")
    if not token:
        return HttpResponse("Kein Token übergeben.", status=400)

    try:
        daten = decode_jwt(token)
        print(f"Raspberry daten: {daten}")
        print(f"Raspberry user-id: {daten['user_id']}")
    except Exception:
        return HttpResponse("Ungültiges oder abgelaufenes Token.", status=401)

    buerger_id = daten.get("user_id")
    if not buerger_id:
        return HttpResponse("Token enthält keine buerger_id.", status=400)

    # Session auf Server B setzen
    request.session["user_id"] = buerger_id

    # Weiter ins Dashboard
    return redirect("geburt") #hier anpassen, weiterleiten auf die Zielseite

def geburt(request):
	if request.method == 'POST':

		if "scan_mutter" in request.POST:
			reader = SimpleMFRC522()
			id, data = reader.read()
			id_mutter = data.strip()
			print(id_mutter)
			request.session["id_mutter"] = id_mutter
			return redirect("geburt")

		if "scan_vater" in request.POST:

			reader = SimpleMFRC522()
			id, data = reader.read()
			id_vater = data.strip()
			print(id_vater)
			request.session["id_vater"] = id_vater
			return redirect("geburt")

		if "geburt" in request.POST:

			nachname = request.POST.get("nachname_geburt")
			vorname = request.POST.get("vorname")
			geburtsdatum = request.POST.get("geburtsdatum")
			id_mutter = request.session["id_mutter"]
			id_vater = request.session["id_vater"]

			person = {"nachname_geburt": nachname, "vorname": vorname, "geburtsdatum": geburtsdatum, "vater_id": id_vater, "mutter_id": id_mutter}
			elterngeld = {"id_vater": id_vater, "id_mutter": id_mutter}
			print(elterngeld)

			neugeboren = requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person, headers={"Connection": "close"})
			print(f"Personenregister: {neugeboren}")

			buerger_id = neugeboren.text
			id_kind = {"id_kind": buerger_id}

			kindergeld = requests.post("http://[2001:7c0:2320:2:f816:3eff:fed4:e456]:1810/kindergeldanlegen", data=id_kind, headers={"Connection": "close"})
			print(f"Kindergeld: {kindergeld}")

			elterngeldanlegen = requests.post("http://[2001:7c0:2320:2:f816:3eff:fed4:e456]:1810/elterngeldanlegen", data=elterngeld, headers={"Connection": "close"})
			print(f"Elterngeld: {elterngeldanlegen}")

			# Zurückgegebene Bürger ID auf RFID Karte schreiben
			reader = SimpleMFRC522()
			reader.write(buerger_id)
			print(f"RFID-Karte beschrieben mit {buerger_id}.")

			# IDs wieder aus der Session löschen 
			del request.session["id_mutter"]
			del request.session["id_vater"]

			return HttpResponse(f"""
                       			<html>
                       				<head>
                       					<title>Herzlichen Glückwunsch!</title>
									</head>
                       					<body style="display:flex; justify-content:center; align-items:center">
                       						<div style="text-align:center">
                       							<h1 style="font-size:3rem; color:#45a049">
                       								Herzlichen Glückwunsch zur Geburt von {vorname}.
												</h1>
											</div>
										</body>
								</html>
								""")
	else:
		return render(request, "app/geburt.html")

def tod(request):
	if request.method == 'POST':

		sterbedatum = request.POST.get("sterbedatum")

		# Bürger ID aus RFID Karte auslesen
		reader = SimpleMFRC522()
		id, data = reader.read()
		# Keine Ahnung wo sich ein unsichtbares Zeichen dazugemogelt hat - aber mit strip() gehts!
		id_person = data.strip()
		print(id_person)

		response = requests.get(f"http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/api/person/{id_person}", headers={"Connection": "close"})
		print(response)
		personendaten = response.json()
		print(personendaten)
		vorname = personendaten["vorname"]
		if personendaten["nachname_neu"]:
			nachname = personendaten["nachname_neu"]
		else:
			nachname = personendaten["nachname_geburt"]
		name_person = f"{vorname} {nachname}"

		person = {"buerger_id": id_person, "sterbedatum": sterbedatum}

		response = requests.post("http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/personenstandsregister_api", data=person, headers={"Connection": "close"})
		print(response)

		return HttpResponse(f"""
                       			<html>
                       				<head>
                       					<title>Herzlichen Glückwunsch!</title>
									</head>
                       					<body style="display:flex; justify-content:center; align-items:center">
                       						<div style="text-align:center">
                       							<h1 style="font-size:3rem; color:#45a049">
                       								{name_person} ist am {sterbedatum} verstorben. Requiescat in Pace.
												</h1>
											</div>
										</body>
								</html>
							""")

	else:
		return render(request, "app/tod.html")