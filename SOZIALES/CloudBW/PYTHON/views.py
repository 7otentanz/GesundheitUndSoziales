from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import requests
import datetime

static_soz = "/var/www/static/sozialleistungen"
static_rente = "/var/www/static/rente"
static_arbeit = "/var/www/static/arbeitslos"

def start(request):
	return render(request, "app/start.html")

@csrf_exempt
def elterngeldanlegen(request):
	if request.method == 'POST':
		id_sorgebrechtigter1 = request.POST.get("id_sorgebrechtigter1")
		id_sorgebrechtigter2 = request.POST.get("id_sorgebrechtigter2")
		datum = datetime.date.today()

		with open(f"{static_soz}/elterngeld.json", "r", encoding="utf-8") as datei:
			elterngeldregister = json.load(datei)

		#Eltern noch nicht in Elterngeldbereichtigte.json
		if id_sorgebrechtigter1 not in elterngeldregister["berechtigte"]:
			elterngeldregister["berechtigte"].append({"id_sorgebrechtigter1" : id_sorgebrechtigter1, "Datum" : datum})
		if id_sorgebrechtigter2 not in elterngeldregister["berechtigte"]:
			elterngeldregister["berechtigte"].append({"id_sorgebrechtigter2" : id_sorgebrechtigter2, "Datum" : datum})
		
		#Eltern bereits vorhanden
		if id_sorgebrechtigter1 in elterngeldregister["berechtigte"]:
			elterngeldregister["berechtigte"].remove({"Datum" : datum})
			elterngeldregister["berechtigte"].append({"Datum" : datum})
		if id_sorgebrechtigter2 in elterngeldregister["berechtigte"]:
			elterngeldregister["berechtigte"].remove({"Datum" : datum})
			elterngeldregister["berechtigte"].append({"Datum" : datum})
		

		with open(f"{static_soz}/elterngeld.json", "w", encoding="utf-8") as datei:
			json.dump(elterngeldregister, datei, indent=4)
		
		return HttpResponse("OK", status=200)
	
@csrf_exempt
def elterngeldberechtigte(request):
	with open(f"{static_soz}/elterngeld.json", "r", encoding="utf-8") as datei:
		elterngeldberechtigte = json.load(datei)
		
		return JsonResponse(elterngeldberechtigte)
	
@csrf_exempt
def kindergeldanlegen(request):
	if request.method == 'POST':
		id_kind = request.POST.get("id_kind")
		datum = datetime.date.today()

		with open(f"{static_soz}/kindergeld.json", "r", encoding="utf-8") as datei:
			kindergeldberechtigte = json.load(datei)

		if id_kind not in kindergeldberechtigte["berechtigte"]:
			kindergeldberechtigte["berechtigte"].append({"id_kind" : id_kind, "Datum" : datum})

		with open(f"{static_soz}/kindergeld.json", "w", encoding="utf-8") as datei:
			json.dump(kindergeldberechtigte, datei, indent=4)
		
		return HttpResponse("OK", status=200)
	
@csrf_exempt
def kindergeldberechtigte(request):
	with open(f"{static_soz}/kindergeld.json", "r", encoding="utf-8") as datei:
		kindergeldberechtigte = json.load(datei)
		
		return JsonResponse(kindergeldberechtigte)
	

@csrf_exempt
def api_rentenbetraege(request):

	if request.method == "GET":
		with open (f"{static_rente}/rentenregister.json", "r", encoding="utf-8") as datei:
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
		with open (f"{static_arbeit}/arbeitslosenregister.json", "r", encoding="utf-8") as datei:
			arbeitslosenregister = json.load(datei)

		daten = []

		for arbeitsloser in list(arbeitslosenregister["personen"]):
			daten.append({
				"uid" : arbeitsloser["uid"],
				"arbeitslosengeld" : arbeitsloser["arbeitslosengeld"]})
		
		return JsonResponse({"personen": daten}, json_dumps_params={'indent': 4})

			

