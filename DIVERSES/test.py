import requests
import json

test_eltern = requests.get("http://[2001:7c0:2320:2:f816:3eff:fe79:999d]/ro/gesetz_api/12")
test_kinder = requests.get("http://[2001:7c0:2320:2:f816:3eff:fe79:999d]/ro/gesetz_api/11")

eltern = test_eltern.json()
kinder = test_kinder.json()


print(eltern["api_relevant"][0])
print(kinder["api_relevant"][0])