#import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
#from django.http import HttpResponse, JsonResponse

static_soz = "/var/www/static/sozialleistungen"
#static_soz = "C:/Laura/Studium/Ludwigsburg/2025_26_WiSe/Inf/GesundheitUndSoziales/SOZIALES/CloudBW/STATIC/sozialleistungen" #Laptop


def kindergeldsync():

    with open(f"{static_soz}/kindergeld.json", "r", encoding="utf-8") as datei:
        kindergeldregister = json.load(datei)
        print (kindergeldregister)

    heute = datetime.date.today()
    ein_jahr = heute - relativedelta(years=25)
    

    #soll nur Datum prüfen --> wenn länger als 25 Jahr her, dann löschen

    for berechtigte in list(kindergeldregister["berechtigte"]):
        eintrag_datum = datetime.datetime.strptime(berechtigte["datum"], '%Y-%m-%d').date()

        if eintrag_datum < ein_jahr:
            kindergeldregister["berechtigte"].remove(berechtigte)

  

    with open(f"{static_soz}/kindergeld.json", "w", encoding="utf-8") as datei:
        json.dump(kindergeldregister, datei, indent=4)

    with open(f"{static_soz}/kindergeldaktualisierung.txt", "w") as datei:
        datei.write(f"Kindergeldregister aktualisiert am {datetime.datetime.now()}.")
    
#        return HttpResponse("OK", status=200)
    
kindergeldsync()


    
