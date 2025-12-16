from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

static = "/var/www/static"

def start(request):
	return render(request, "app/start.html")