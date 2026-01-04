from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

static = "/var/www/static"

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

def termintest(request):
	if request.method == 'POST':

		spez = request.POST.get("spezialisierung")
		stand = request.POST.get("standort")
		arzt = request.POST.get("arzt")

		terminjson = {
			"Spez": spez,
			"Stand": stand,
			"Arzt": arzt
		}

	return HttpResponse(str(terminjson))