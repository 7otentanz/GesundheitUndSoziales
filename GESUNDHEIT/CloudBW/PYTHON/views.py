from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

static = "/var/www/static"

@csrf_exempt
def geburt(request):
	if request.method == 'POST':
		text = str(request.POST.get("nachname_geburt"))
		with open("/var/www/static/person.txt", "w") as datei:
			datei.write(text)
	return HttpResponse("ok")