from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

#def test(request):
#	return HttpResponse("Hallo.")

einwohnerliste = [
{"id": 123, "name": "Laura Pfefferkorn"},
{"id": 234, "name": "Tim Hauser"},
]


def name(request, name):
	return HttpResponse(f"Hello my name is {name}.")

def einwohner(request, id):
	for eintrag  in einwohnerliste:
		if eintrag["id"] == id:
			return HttpResponse(f"{eintrag['name']} gefunden")
		else:
			return HttpResponse("Nope.")
#@csrf_exempt
#def geburt(request, person):
#	print(os.getcwd())
#	with open("/var/www/static/person.txt", "w") as datei:
#		datei.write(person)

@csrf_exempt
def geburt(request):
	if request.method == 'POST':
		text = str(request.POST.get("nachname_geburt"))
		with open("/var/www/static/person.txt", "w") as datei:
			datei.write(text)
	return HttpResponse("ok")
