from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

static = "/var/www/static"

def start(request):
	return render(request, "app/start.html")

def termin(request):
	with open(f"{static}/arztregister.json", "r") as datei:
		arztregister = json.load(datei)

	# Spezialisierungen und Standorte aus Arztregister auslesen und jeder Spezialisierung id und standort das arztes zuweisen
	spezialisierungen = []
	for arzt in list(arztregister["personen"]):
		spezialisierung = arzt["spezialisierung"]
		
		if spezialisierung not in spezialisierungen:
			spezialisierungen.append(spezialisierung)

	standorte = []
	gewaehltespezialisierung = ""

	# Spezialisierung abfangen
	if request.method == 'POST':
		gewaehltespezialisierung = request.POST.get("spezialisierung")

		# Standorte auslesen die auf die gewählte Spezialisierung passen
		for arzt in list(arztregister["personen"]):
			if arzt["spezialisierung"] == gewaehltespezialisierung:
				standorte.append(arzt["standort"])
	
	context = {
		"spezialisierungen": spezialisierungen,
		"standorte": standorte,
		"gewaehltespezialisierung": gewaehltespezialisierung
	}
		
	return render(request, "app/termin.html", context)