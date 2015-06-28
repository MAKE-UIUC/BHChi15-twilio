import os
from flask import Flask, request, redirect, session, make_response
from datetime import datetime, timedelta
import twilio.twiml
#import yaml
import config
import requests
import json



SECRET_KEY =  config.key 
GEOCODE_KEY = config.geocode_key

app = Flask(__name__)
 
def helper(obj):
    return obj['approx_dist']

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    name = request.values.get('Body', None)
    if name is None:
        replyString = "Error in Twilio"
        resp = twilio.twiml.Response()
        resp.message(replyString)
        return str(resp)
    medicine = name.split('near')[0].strip()
    location = name.split('near')[1].strip()
    API_KEY = config.geocode_key
    Address = location 
    baseurl = "http://steam.intense.io/api/v1/users/pharmacies?medicine_name="
    radius = "100"


    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + Address + "&key="+API_KEY)

    jsonResponse = json.loads(r.text)
    try:
        latitude = json.dumps(jsonResponse['results'][0]['geometry']['location']['lat'])
        longitude = json.dumps(jsonResponse['results'][0]['geometry']['location']['lng'])
    except:
        replyString = "Location not found. Try another description of the location"
        resp = twilio.twiml.Response()
        resp.message(replyString)
        return str(resp)
    

    urlString = baseurl + medicine + "&latitude=" + latitude + "&longitude=" + longitude + "&radius=" + radius

    r = requests.get(urlString)
    jsonResponse = json.loads(r.text)
    num_locations = int(jsonResponse['num_locations'])
    if num_locations == 0:
        replyString = "No locations with specified med found."
        resp = twilio.twiml.Response()
        resp.message(replyString)
        return str(resp)

    address_list = jsonResponse['locations']
    address_list.sort(key=lambda obj: obj['approx_dist'])

    address_found = address_list[0]['address']
    medicine_found = address_list[0]['medicine_name']
    price = address_list[0]['price']
    store_name = address_list[0]['name']

    
    resp = twilio.twiml.Response()
    replyString = medicine_found + " can be found at " + store_name + " " + address_found
    replyString2 = "To prepay for pickup, text " + "\"" + price + " to order@medsnear.me note ID:49x20d" + "\"" +  "to 729725" 
    replyString3 = "Forward this to a friend if no internet is avaliable, and they are willing to pay for you."    
    replyString = replyString  + "\n" + "---------"  + "\n" + replyString2 + "\n" + "---------" + "\n" + replyString3
    resp.message(replyString)
    return str(resp) 
 
if __name__ == "__main__":
    app.run(debug=True)