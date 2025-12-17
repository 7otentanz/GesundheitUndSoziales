from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import requests


static = "/var/www/static"

def start(request):
	return render(request, "app/start.html")

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
def elterngeldberechtigte(request):
	with open(f"{static}/elterngeld.json", "r", encoding="utf-8") as datei:
		elterngeldberechtigte = json.load(datei)
		
		return JsonResponse(elterngeldberechtigte)
	

@csrf_exempt
def api_rentenbetraege(request):

	if request.method == "GET":
		with open (f"{static}/rentenregister.json", "r", encoding="utf-8") as datei:
			rentenregister = json.load(datei)

		daten = []

		for rentner in list(rentenregister["personen"]):
			daten.append({
				"uid" : rentner["uid"],
				"rentenbetrag" : rentner["rentenbetrag"]})
		
		return JsonResponse({"personen": daten}, json_dumps_params={'indent': 4})
	

@csrf_exempt
def api_arbeitslosenbetraege(request):

	if request.method == "GET":
		with open (f"{static}/arbeitslosenregister.json", "r", encoding="utf-8") as datei:
			arbeitslosenregister = json.load(datei)

		daten = []

		for arbeitsloser in list(arbeitslosenregister["personen"]):
			daten.append({
				"uid" : arbeitsloser["uid"],
				"arbeitslosengeld" : arbeitsloser["arbeitslosengeld"]})
		
		return JsonResponse({"personen": daten}, json_dumps_params={'indent': 4})

			

