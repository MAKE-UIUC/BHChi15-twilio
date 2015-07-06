import requests
import json
import config

baseurl = "http://steam.intense.io/api/v1/users/pharmacies?medicine_name="
medicine = "Claritin"
latitude = "41.2"
longitude = "-87.5"
radius = "100"

def helper(obj):
	return obj['approx_dist']

urlString = baseurl + medicine + "&latitude=" + latitude + "&longitude=" + longitude + "&radius=" + radius

r = requests.get(urlString)
jsonResponse = json.loads(r.text)
num_locations = json.dumps(jsonResponse['num_locations'])
if num_locations is 0:
	print "No locations with specified med found"
address_list = jsonResponse['locations']
address_list.sort(key=lambda obj: obj['approx_dist'])



address_found = json.dumps(address_list[0]['address'])
medicine_found = json.dumps(address_list[0]['medicine_name'])
price = json.dumps(address_list[0]['price'])
store_name = json.dumps(address_list[0]['name'])

print address_found
print medicine_found
print price
print store_name