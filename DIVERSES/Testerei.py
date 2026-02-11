import requests

id_person = "3e2ff254-eaa7-426b-abbe-b2cf41bfd8c4"

response = requests.get(f"http://[2001:7c0:2320:2:f816:3eff:fef8:f5b9]:8000/einwohnermeldeamt/api/person/{id_person}", headers={"Connection": "close"})

personendaten = response.json()
print(personendaten)
vorname = personendaten["vorname"]
if personendaten["nachname_neu"]:
	nachname = personendaten["nachname_neu"]
else:
	nachname = personendaten["nachname_geburt"]
name_person = f"{vorname} {nachname}"

print(personendaten["vorname"])