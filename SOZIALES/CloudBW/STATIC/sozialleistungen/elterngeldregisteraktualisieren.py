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
        #print (elterngeldregister)

    #Eltern noch nicht in Elterngeldbereichtigte.json
    heute = datetime.date.today()
    ein_jahr = heute - relativedelta(years=1)
    print (f"heute:  {heute}    ein Jahr: {ein_jahr}" ) 
    

    #soll nur Datum prüfen --> wenn

    for berechtigte in list(elterngeldregister["berechtigte"]):
        eintrag_datum = datetime.datetime.strptime(berechtigte["datum"], '%Y-%m-%d').date()
         
        #print (eintrag_datum)

        if eintrag_datum < ein_jahr:
            elterngeldregister["berechtigte"].remove(berechtigte)



    with open(f"{static_soz}/elterngeld.json", "w", encoding="utf-8") as datei:
        json.dump(elterngeldregister, datei, indent=4)

    with open(f"{static_soz}/elterngeldaktualisierung.txt", "w") as datei:
        datei.write(f"Elterngeldregister aktualisiert am {datetime.datetime.now()}.")
        #print(elterngeldregister)
    
#        return HttpResponse("OK", status=200)
    
elterngeldsync()


    
