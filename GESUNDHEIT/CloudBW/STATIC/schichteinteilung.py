import json
import datetime

static = "/var/www/static"

schichten = ["früh", "spät", "nacht", "frei"]

def schichteneinteilen():

    with open(f"{static}/arztregister.json", "r", encoding="utf-8") as datei:
        arztregister = json.load(datei)
        print(arztregister)

    # Listen mit Standorten anlegen als Grundlage für die Schichtverteilung
    standorte = dict()
    for arzt in arztregister["personen"]:
        standort = arzt["standort"]
        if standort not in standorte:
            standorte[standort] = list()
        standorte[standort].append(arzt)

    for standort, aerzte in standorte.items():

        schichtzaehler = {"früh": 0, "spät": 0, "nacht": 0, "frei": 0}
        neueAerzte = list()

        for arzt in aerzte:
            # bereits eingetragene Ärzte haben auch schon eine Schicht
            if "schicht" in arzt:
                schichtzaehler[arzt["schicht"]] += 1
            # neue Ärzte aber nicht
            else:
                neueAerzte.append(arzt)
        
        # neue Ärzte der Schicht mit den wenigsten Ärzten hinzufügen
        for arzt in neueAerzte:
            kleinsteschicht = schichten[0]
            kleinsteanzahl = schichtzaehler[kleinsteschicht]

            for schicht in schichten:
                if schichtzaehler[schicht] <= kleinsteanzahl:
                    kleinsteschicht = schicht
                    kleinsteanzahl = schichtzaehler[schicht]

            arzt["schicht"] = kleinsteschicht
            schichtzaehler[kleinsteschicht] += 1

        #Alle Ärzte einmal rotieren
        for arzt in aerzte:
            if "schicht" in arzt:
                letzteSchicht = arzt["schicht"]
                letzterIndex = schichten.index(letzteSchicht)
                if letzterIndex == 3:
                    neuerIndex = 0
                else:
                    neuerIndex = letzterIndex +1
                neueSchicht = schichten[neuerIndex]
                arzt["schicht"] = neueSchicht
                schichtzaehler[neueSchicht] += 1

    with open(f"{static}/arztregister.json", "w", encoding="utf-8") as datei:
        json.dump(arztregister, datei, indent=4)

    with open(f"{static}/aktualisierung.txt", "w") as datei:
        datei.write(f"Arztregister aktualisiert am {datetime.datetime.now()}.")

schichteneinteilen()