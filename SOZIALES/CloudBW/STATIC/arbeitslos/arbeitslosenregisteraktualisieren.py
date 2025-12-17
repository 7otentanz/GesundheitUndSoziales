import requests
import json
import datetime

static = "/var/www/static/arbeitslos" #server
#static = "C:/Laura/Studium/Ludwigsburg/2025_26_WiSe/Inf/GesundheitUndSoziales/SOZIALES/CloudBW/STATIC" #Laptop

def arbeitslosensync():
    response = requests.get("http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/personenliste/arbeitslos")
    arbeitslosenliste = response.json()
    print(arbeitslosenliste)

    with open(f"{static}/arbeitslosenregister.json", "r", encoding="utf-8") as datei:
        arbeitslosenregister = json.load(datei)
        print(arbeitslosenregister)

        #Prüfen, ob alle Renter noch in Rentenliste von A&Q vorhanden sind, die in Sozialamt bekannt sind; falls nicht: entfernen
    for arbeitsloser in list(arbeitslosenregister["personen"]):
        if arbeitsloser["uid"] not in arbeitslosenliste.values():
            arbeitslosenregister["personen"].remove(arbeitsloser)
        else:
            continue #Platzhalter
        print(arbeitslosenregister)

        #Renter auslesen und alle Renter dem Register hinzufügen
    for arbeitsloser in arbeitslosenliste["personen"]:
        buerger_id = arbeitsloser["uid"]
        print(buerger_id)

        #Rentner bereits in Register, es wird nichts mehr getan
        if buerger_id in list(arbeitslosenregister["personen"]):
            continue

        #Renter noch nicht registriert, muss noch hinzugefügt werden
        elif buerger_id not in list(arbeitslosenregister["personen"]):
            letztes_gehalt = arbeitsloser["letztes_gehalt"]
            arbeitslosengeld = letztes_gehalt * 0.8
            if arbeitslosengeld < 1500:
                arbeitslosengeld = 1500
            arbeitslosenregister["personen"].append({"uid":buerger_id, "letztes_gehalt":letztes_gehalt, "arbeitslosengeld":arbeitslosengeld})

        else:
            continue #Platzhalter

    print(arbeitslosenregister)

    with open(f"{static}/arbeitslosenregister.json", "w", encoding="utf-8") as datei:
        json.dump(arbeitslosenregister, datei, indent=4)

    with open(f"{static}/arbeitsloseaktualisieren.txt", "w") as datei:
        datei.write(f"Arbeteitslosenregister aktuallisiert am {datetime.datetime.now()}.")



arbeitslosensync()