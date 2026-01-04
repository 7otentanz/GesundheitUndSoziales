#import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
#from django.http import HttpResponse, JsonResponse

static_soz = "/var/www/static/sozialleistungen"
#static_soz = "C:/Laura/Studium/Ludwigsburg/2025_26_WiSe/Inf/GesundheitUndSoziales/SOZIALES/CloudBW/STATIC/sozialleistungen" #Laptop


def elterngeldsync():

    with open(f"{static_soz}/elterngeld.json", "r", encoding="utf-8") as datei:
        elterngeldregister = json.load(datei)
        print (elterngeldregister)

    #Eltern noch nicht in Elterngeldbereichtigte.json
    heute = datetime.date.today()
    ein_jahr = heute - relativedelta(years=1)
    

    #soll nur Datum prüfen --> wenn

    for berechtigte in elterngeldregister["berechtigte"]:
        eintrag_datum = datetime.date(berechtigte["Datum"])

        if heute - eintrag_datum > ein_jahr:
            elterngeldregister["berechtigte"].remove(berechtigte)




    
    # if id_sorgebrechtigter1 not in list(elterngeldregister["berechtigte"]):
    #     elterngeldregister["berechtigte"].append({"id_sorgebrechtigter1" : id_sorgebrechtigter1, "Datum" : datum})
    # if id_sorgebrechtigter2 not in list(elterngeldregister["berechtigte"]):
    #     elterngeldregister["berechtigte"].append({"id_sorgebrechtigter2" : id_sorgebrechtigter2, "Datum" : datum})
                
    # if id_sorgebrechtigter1 in list(elterngeldregister["berechtigte"]):
    #     for eintrag in elterngeldregister["berechtigte"]:
    #         eintrag["Datum"] = datum


    #Eltern bereits in Elterngeldregister.json --> neues Kind, aktualisierung Datum


    

    with open(f"{static_soz}/elterngeld.json", "w", encoding="utf-8") as datei:
        json.dump(elterngeldregister, datei, indent=4)

    with open(f"{static_soz}/elterngeldaktualisierung.txt", "w") as datei:
        datei.write(f"Elterngeldregister aktualisiert am {datetime.datetime.now()}.")
    
#        return HttpResponse("OK", status=200)
    
elterngeldsync()


    
