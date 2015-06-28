import requests
import json

API_KEY = ""

r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key="+API_KEY)
print r.text