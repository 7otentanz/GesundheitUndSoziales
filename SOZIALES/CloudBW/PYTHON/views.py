from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import requests
import datetime
from project.jwt_tooling import decode_jwt

static_soz = "/var/www/static/sozialleistungen"
static_rente = "/var/www/static/rente"
static_arbeit = "/var/www/static/arbeitslos"

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

@csrf_exempt
def elterngeldanlegen(request):
	if request.method == 'POST':
		id_vater = request.POST.get("id_vater")
		id_mutter = request.POST.get("id_mutter")
		datum = str(datetime.date.today())
		gesetz_elterngeld = requests.get("http://[2001:7c0:2320:2:f816:3eff:fe79:999d]/ro/gesetz_api/12")
 
		print(f"1: {id_vater}, 2: {id_mutter}")

		with open(f"{static_soz}/elterngeld.json", "r", encoding="utf-8") as datei:
			elterngeldregister = json.load(datei)
			berechtigte = elterngeldregister["berechtigte"]
			
			neuer_betrag = gesetz_elterngeld.json()
			betrag = neuer_betrag["api_relevant"][0]
			elterngeldregister["betrag"] = betrag


		in_register_vorhanden = False

		for person in berechtigte:
			if person["sorgeberechtigter"] == id_vater:
				person["datum"] = datum
				in_register_vorhanden = True
				break
			
		if in_register_vorhanden == False:
			elterngeldregister["berechtigte"].append({"sorgeberechtigter" : id_vater, "datum" : datum})

		in_register_vorhanden = False

		for person in berechtigte:
			if person["sorgeberechtigter"] == id_mutter:
				person["datum"] = datum
				in_register_vorhanden = True
				break
			
		if in_register_vorhanden == False:
			elterngeldregister["berechtigte"].append({"sorgeberechtigter" : id_mutter, "datum" : datum})

		
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
		datum = str(datetime.date.today())
		gesetz_kindergeld = requests.get("http://[2001:7c0:2320:2:f816:3eff:fe79:999d]/ro/gesetz_api/11")
		print(datum)

		with open(f"{static_soz}/kindergeld.json", "r", encoding="utf-8") as datei:
			kindergeldberechtigte = json.load(datei)
			neuer_betrag = gesetz_kindergeld.json()


			betrag = neuer_betrag["api_relevant"][0]
			kindergeldberechtigte["betrag"] = betrag

		kindergeldberechtigte["berechtigte"].append({"id_kind" : id_kind, "datum" : datum})

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
	

@csrf_exempt
def api_sozialleistungen(request, user_id):

	if request.method == "GET":
		buerger_id = user_id

		with open (f"{static_arbeit}/arbeitslosenregister.json", "r", encoding="utf-8") as datei:
			arbeitslosenregister = json.load(datei)

		with open (f"{static_soz}/elterngeld.json", "r", encoding="utf-8") as datei:
			elterngeldregister = json.load(datei)
		with open (f"{static_soz}/kindergeld.json", "r", encoding="utf-8") as datei:
			kindergeldregister = json.load(datei)

		with open (f"{static_rente}/rentenregister.json", "r", encoding="utf-8") as datei:
			rentenregister = json.load(datei)

		daten = []

		# for person in list(arbeitslosenregister["person"]):
		# 	if person["buerger_id"] == buerger_id:
		# 		daten.append({
		# 			"arbeitslosengeld" : person["arbeitslosengeld"]})
		
		for person in list (elterngeldregister["berechtigte"]):
			if person["sorgeberechtigter"] == buerger_id:
				daten.append({
					"Elterngeld Datum erhalt ab: " : person["datum"],
					"Elterngeldbetrag" : elterngeldregister.get("betrag")})

		for person in list (kindergeldregister["berechtigte"]):
			if person["id_kind"] == buerger_id:
				daten.append({
					"Kindergeld Datum erhalt ab: " : person["datum"],
					"Kindergeldbetrag" : kindergeldregister.get("betrag")})

		for person in list (rentenregister["personen"]):
			if person["uid"] == buerger_id:
				daten.append({
					"Rentenbetrag: " : person["rentenbetrag"], 
				  })
		

		return JsonResponse({"Sozialleistungen": daten}, json_dumps_params={'indent': 4})
	

def sozialleistungen(request):
	buerger_id = request.session.get("user_id")

	api = f"http://[2001:7c0:2320:2:f816:3eff:fed4:e456]:1810/api_sozialleistungen/{buerger_id}"

	response = requests.get(api)
	daten = response.json()
	print("Daten ", daten)
	return render(request, "app/sozialleistungen.html", {"user_id" : buerger_id, "daten" : daten})


			

