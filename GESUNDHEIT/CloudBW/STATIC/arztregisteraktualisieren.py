import requests
import json
import random
import datetime

static = "/var/www/static"

spezialisierungen = ["Neurologe", "Pulmologe", "Kardiologe", "Zahnarzt", "Dentalchirurg", "Unfallchirurg", "Allgemeinmediziner", "Gynäkologe", "Psychiater"]

def arztregistrieren():

    response = requests.get("http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/personenliste/arzt")
    arztliste = response.json()
    print(arztliste)

    with open(f"{static}/arztregister.json", "r", encoding="utf-8") as datei:
        arztregister = json.load(datei)
        print(arztregister)

    #Prüfen ob alle Ärzte aus dem Register auch wirklich noch Ärzte sind. Falls nicht entfernen.
    for arzt in list(arztregister["personen"]):
        if arzt["uid"] not in arztliste.values():
            arztregister["personen"].remove(arzt)   
        else:
            continue #Platzhalter
        print(arztregister)

    #Arztliste auslesen und alle Ärzte dem Register hinzufügen
    for arzt in arztliste["personen"]:
        buerger_id = arzt["uid"]
        print(buerger_id)

        if buerger_id in list(arztregister["personen"]):
            continue

        #Arzt aus der API-Liste unserem Arzt-Register hinzufügen - wenn er noch nicht registriert ist
        elif buerger_id not in list(arztregister["personen"]):
            spezialisierung = random.choice(spezialisierungen)
            standort = f"{arzt['arbeitgeber']}, {arzt['adresse']}"
            arztregister["personen"].append({"uid": buerger_id, "spezialisierung": spezialisierung, "standort": standort})

        else:
            continue #Platzhalter
    
    print(arztregister)

    with open(f"{static}/arztregister.json", "w", encoding="utf-8") as datei:
        json.dump(arztregister, datei, indent=4)

    with open(f"{static}/aktualisierung.txt", "w") as datei:
        datei.write(f"Arztregister aktualisiert am {datetime.datetime.now()}.")

arztregistrieren()
