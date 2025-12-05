import requests
import json
import datetime

#static = "/var/www/static" #server
static = "C:/Laura/Studium/Ludwigsburg/2025_26_WiSe/Inf/GesundheitUndSoziales/SOZIALES/CloudBW/STATIC" #Laptop

def renteregistrieren():
    response = requests.get("http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/personenliste/rente")
    rentenliste = response.json()
    print(rentenliste)

    with open(f"{static}/rentenregister.json", "r", encoding="utf-8") as datei:
        rentenregister = json.load(datei)
        print(rentenregister)

        #Prüfen, ob alle Renter noch in Rentenliste von A&Q vorhanden sind, die in Sozialamt bekannt sind; falls nicht: entfernen
    for rentner in list(rentenregister["personen"]):
        if rentner["uid"] not in rentenliste.values():
            rentenregister["personen"].remove(rentner)
        else:
            continue #Platzhalter
    print(rentenregister)

        #Renter auslesen und alle Renter dem Register hinzufügen
    for rentner in rentenliste["personen"]:
        buerger_id = rentner["uid"]
        print(buerger_id)

        #Rentner bereits in Register, es wird nichts mehr getan
        if buerger_id in list(rentenregister["personen"]):
            continue

        #Renter noch nicht registriert, muss noch hinzugefügt werden
        elif buerger_id not in list(rentenregister["personen"]):
            letztes_gehalt = rentner["letztes_gehalt"]
            rentenregister["personen"].append({"uid":buerger_id, "lestztes_gehalt":letztes_gehalt})

        else:
            continue #Platzhalter

    print(rentenregister)

    with open(f"{static}/rentenregister.json", "w", encoding="utf-8") as datei:
        json.dump(rentenregister, datei, indent=4)

    with open(f"{static}/aktualisierung.txt", "w") as datei:
        datei.write(f"Rentenregsiter aktuallisiert am {datetime.datetime.now()}.")



renteregistrieren()