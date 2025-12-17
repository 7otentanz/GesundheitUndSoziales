import requests
import json
import datetime

static = "/var/www/static/beamte" #server
#static = "C:/Laura/Studium/Ludwigsburg/2025_26_WiSe/Inf/GesundheitUndSoziales/SOZIALES/CloudBW/STATIC" #Laptop

def beamterync():

    response = requests.get("http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/personenliste/beamter")
    beamtenliste = response.json()
    print(beamtenliste)

    with open(f"{static}/beamtenregister.json", "r", encoding="utf-8") as datei:
        beamtenregister = json.load(datei)
        print(beamtenregister)

        #Prüfen, ob alle Renter noch in beamtenliste von A&Q vorhanden sind, die in Sozialamt bekannt sind; falls nicht: entfernen
    for beamter in list(beamtenregister["personen"]):
        if beamter["uid"] not in beamtenliste.values():
            beamtenregister["personen"].remove(beamter)
        else:
            continue #Platzhalter
        print(beamtenregister)

        #Renter auslesen und alle Renter dem Register hinzufügen
    for beamter in beamtenliste["personen"]:
        buerger_id = beamter["uid"]
        print(buerger_id)

        #beamter bereits in Register, es wird nichts mehr getan
        if buerger_id in list(beamtenregister["personen"]):
            continue

        #Renter noch nicht registriert, muss noch hinzugefügt werden
        elif buerger_id not in list(beamtenregister["personen"]):
            beamtenregister["personen"].append({"uid":buerger_id})

        else:
            continue #Platzhalter

    print(beamtenregister)

    with open(f"{static}/beamtenregister.json", "w", encoding="utf-8") as datei:
        json.dump(beamtenregister, datei, indent=4)

    with open(f"{static}/beamtenregisteraktualisieren.txt", "w") as datei:
        datei.write(f"Beamtenregister aktuallisiert am {datetime.datetime.now()}.")



beamterync()