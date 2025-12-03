import requests
import json

def renteregistrieren():
    response = requests.get("http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/personenliste/rente")
    rentenliste = response.json()

    for rentner in rentenliste:
        buerger_id = rentner ["uid"]
        letztes_gehalt = rentner ["letztes_gehalt"]