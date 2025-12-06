from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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

def elterngeldberechtigte(request):
	with open(f"{static}/elterngeld.json", "r", encoding="utf-8") as datei:
		elterngeldberechtigte = json.load(datei)
		
		return JsonResponse(elterngeldberechtigte)

@csrf_exempt
def elterngeldanlegen(request):
	if request.method == 'POST':
		id_mutter = request.POST.get("id_mutter")
		id_vater = request.POST.get("id_vater")

		with open(f"{static}/elterngeld.json", "r", encoding="utf-8") as datei:
			elterngeldberechtigte = json.load(datei)

		elterngeldberechtigte["berechtigte"].append(id_mutter)
		elterngeldberechtigte["berechtigte"].append(id_vater)

		with open(f"{static}/elterngeld.json", "w", encoding="utf-8") as datei:
			json.dump(elterngeldberechtigte, datei, indent=4)
		
		return HttpResponse("OK", status=200)
	

@csrf_exempt
def renteregistrieren(request):
	if request.method == 'POST':
		buerger_id = request.POST.get("buerger_id")
		letztes_gehalt = request.POST.get("letzts_gehalt")

		with open(f"{static}/rentenregister.json", "r", encoding="utf8") as datei:
			rentenregister = json.load(datei)
		rentenregister[buerger_id] = {"letztes_gehalt" : letztes_gehalt}

		with open (f"{static}/rentenregister.json", "w", encoding="utf-8") as datei:
			json.dump(rentenregister, datei, indent=4)

		return HttpResponse("OK", status=200)