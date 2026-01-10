import requests
import json
import random
import datetime

static = "/var/www/static"

spezialisierungen = ["Neurologe", "Pulmologe", "Kardiologe", "Zahnarzt", "Dentalchirurg", "Unfallchirurg", "Allgemeinmediziner", "Gynäkologe", "Psychiater"]
schichten = ["Früh", "Spät", "Nacht", "Frei"]

def arztregistrieren():

    response = requests.get("http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/personenliste/arzt", headers={"Connection": "close"})
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

    # Listen mit Standorten anlegen als Grundlage für die Schichtverteilung
    standorte = dict()
    for arzt in arztregister["personen"]:
        standort = arzt["standort"]
        if standort not in standorte:
            standorte[standort] = list()
        standorte[standort].append(arzt)

    for standort, aerzte in standorte.items():

        frueh = 0
        spaet = 0
        nacht = 0
        frei = 0

        # Rotation nach Kalenderwoche
        kalenderwoche = datetime.date.today().isocalendar().week

        if kalenderwoche in [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49]:
            frueh += 1
        if kalenderwoche in [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50]:
            spaet += 1
        if kalenderwoche in [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51]:
            nacht += 1
        if kalenderwoche in [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]:
            frei += 1

        for arzt in aerzte:

            if frueh <= spaet and frueh <= nacht and frueh <= frei:
                arzt["schicht"] = "früh"
                frueh += 1
            
            elif spaet <= frueh and spaet <= nacht and spaet <= frei:
                arzt["schicht"] = "spät"
                spaet += 1

            elif nacht <= frueh and nacht <= spaet and nacht <= frei:
                arzt["schicht"] = "nacht"
                nacht += 1

            else:
                arzt["schicht"] = "frei"
                frei += 1

    with open(f"{static}/arztregister.json", "w", encoding="utf-8") as datei:
        json.dump(arztregister, datei, indent=4)

    with open(f"{static}/aktualisierung.txt", "w") as datei:
        datei.write(f"Arztregister aktualisiert am {datetime.datetime.now()}.")

arztregistrieren()
