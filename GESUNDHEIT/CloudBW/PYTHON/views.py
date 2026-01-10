from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.jwt_tooling import decode_jwt
import os
import json

static = "/var/www/static"

def jwt_login(request):
    token = request.GET.get("token")
    if not token:
        return HttpResponse("Kein Token übergeben.", status=400)

    try:
        daten = decode_jwt(token)
        print(f"Cloud BW daten: {daten}")
        print(f"Cloud BW user-id: {daten["user_id"]}")
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
			if arzt["spezialisierung"] == spezialisierung:
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
				aerzte.append(arzt["uid"]) ### Hier noch ersetzen durch Vor- und Nachnamen nachdem die API steht!

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
		arzt = request.POST.get("arzt")
		datum = request.POST.get("datum")
		uhrzeit = request.POST.get("uhrzeit")

		return HttpResponse(f"{spezialisierung}, {standort}, {arzt}, {datum}, {uhrzeit}.")