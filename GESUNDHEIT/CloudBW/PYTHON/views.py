from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.jwt_tooling import decode_jwt
from ics import Calendar, Event
import requests
import json
import datetime

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
    return redirect("start") #hier anpassen, weiterleiten auf die Zielseite

def start(request):
	buerger_id = request.session.get("user_id")

	if not buerger_id:
		return render(request, "app/start.html")
	else:
		response = requests.get(f"http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/buerger/beruf/{buerger_id}")
		beruf = response.json()["beruf"]

		request.session["beruf"] = beruf
		return render(request, "app/start.html")

def terminspezialisierung(request):
	with open(f"{static}/arztregister.json", "r") as datei:
		arztregister = json.load(datei)

	# Spezialisierungen und Standorte aus Arztregister auslesen und jeder Spezialisierung id und standort das arztes zuweisen
	spezialisierungen = []
	for arzt in list(arztregister["personen"]):
		spezialisierung = arzt["spezialisierung"]
		
		if spezialisierung not in spezialisierungen:
			spezialisierungen.append(spezialisierung)
	
	context = {"spezialisierungen": spezialisierungen}

	return render(request, "app/terminspezialisierung.html", context)
	
def terminstandort(request):
	with open(f"{static}/arztregister.json", "r") as datei:
		arztregister = json.load(datei)	

	# Spezialisierung abfangen
	if request.method == 'POST':
		spezialisierung = request.POST.get("spezialisierung")

		# Standorte auslesen die auf die gewählte Spezialisierung passen
		standorte = []
		for arzt in list(arztregister["personen"]):
			if arzt["spezialisierung"] == spezialisierung and arzt["standort"] not in standorte:
				standorte.append(arzt["standort"])
	
		context = {
			"spezialisierung": spezialisierung,
			"standorte": standorte
		}
			
		return render(request, "app/terminstandort.html", context)

def terminarzt(request):
	with open(f"{static}/arztregister.json", "r") as datei:
		arztregister = json.load(datei)

	if request.method == 'POST':
		spezialisierung = request.POST.get("spezialisierung")
		standort = request.POST.get("standort")

		# Ärzte auslesen die auf Spezialisierung und Standort passen
		aerzte = []
		for arzt in list(arztregister["personen"]):
			if arzt["spezialisierung"] == spezialisierung and arzt["standort"] == standort:
				response = requests.get(f'http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/api/person/{arzt["uid"]}', headers={"Connection": "close"})
				personendaten = response.json()
				vorname = personendaten["vorname"]
				if personendaten["nachname_neu"]:
					nachname = personendaten["nachname_neu"]
				else:
					nachname = personendaten["nachname_geburt"]
				arztname = f"Dr. {vorname} {nachname}"
				aerzte.append({"uid": arzt["uid"], "name": arztname})

		context = {
			"spezialisierung": spezialisierung,
			"standort": standort,
			"aerzte": aerzte
		}

		return render(request, "app/terminarzt.html", context)

def termindatum(request):
	if request.method == 'POST':

		spezialisierung = request.POST.get("spezialisierung")
		standort = request.POST.get("standort")
		arzt = request.POST.get("arzt")

		context = {
			"spezialisierung": spezialisierung,
			"standort": standort,
			"arzt": arzt
		}

		return render(request, "app/termindatum.html", context)

def terminzeit(request):
	if request.method == 'POST':

		spezialisierung = request.POST.get("spezialisierung")
		standort = request.POST.get("standort")
		arzt = request.POST.get("arzt")
		datum = request.POST.get("datum")

		context = {
			"spezialisierung": spezialisierung,
			"standort": standort,
			"arzt": arzt,
			"datum": datum
		}

		return render(request, "app/terminzeit.html", context)
	
def terminendetest(request):
	if request.method == 'POST':

		spezialisierung = request.POST.get("spezialisierung")
		standort = request.POST.get("standort")
		arztuid = request.POST.get("arzt")
		datum = request.POST.get("datum")
		uhrzeit = request.POST.get("uhrzeit")

		response = requests.get(f'http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/api/person/{arztuid}', headers={"Connection": "close"})
		personendaten = response.json()
		vorname = personendaten["vorname"]
		if personendaten["nachname_neu"]:
			nachname = personendaten["nachname_neu"]
		else:
			nachname = personendaten["nachname_geburt"]
		arztname = f"Dr. {vorname} {nachname}"

		startzeit = datetime.datetime.strptime(f"{datum} {uhrzeit}", "%Y-%m-%d %H:%M")
		endzeit = startzeit + datetime.timedelta(minutes=30)

		event = Event()
		event.name = f"Arzttermin: {arztname}, {spezialisierung}, {standort}"
		event.begin = startzeit
		event.end = endzeit
		event.location = standort
		event.description = f"Arzttermin bei:\n{arztname}, {spezialisierung}\nin folgendem Krankenhaus:\n{standort}.\nWir wünschen gute Besserung!"
		#event.uid = f"{uuid.uuid4()}@unserstaat.de"
		
		calendar = Calendar()
		calendar.events.add(event)
		#calendar.extra.append("VERSION:2.0")
		#calendar.extra.append("PRODID:-//unserstaat//arzttermin//DE")

		response = HttpResponse(calendar.serialize(), content_type="text/calendar")
		response["Content-Disposition"] = 'attachment; filename="termin.ics"'
		return response

def videoabgabe(request):
	return render(request, "app/videoabgabe.html")