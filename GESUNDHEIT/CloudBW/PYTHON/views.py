from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

static = "/var/www/static"

@csrf_exempt
def geburt(request):
	if request.method == 'POST':
		text = str(request.POST.get("nachname_geburt"))
		with open("/var/www/static/person.txt", "w") as datei:
			datei.write(text)
	return HttpResponse("ok")

@csrf_exempt
def arztregistrieren(request):
        if request.method == 'POST':
                buerger_id = request.POST.get("buerger_id")
                spezialisierung = request.POST.get("spezialisierung")
                standort = request.POST.get("standort")

                with open(f"{static}/arztregister.json", "r", encoding="utf-8") as datei:
                        arztregister = json.load(datei) 
                arztregister[buerger_id] = {"spezialisierung": spezialisierung, "standort": standort}

                with open(f"{static}/arztregister.json", "w", encoding="utf-8") as datei:
                        json.dump(arztregister, datei, indent=4)

                return HttpResponse("OK", status=200)

