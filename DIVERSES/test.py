import requests

response = requests.get("http://[2001:7c0:2320:2:f816:3eff:feb6:6731]:8000/api/personenliste/arzt", headers={"Connection": "close"})
arztliste = response.json()
print(arztliste)