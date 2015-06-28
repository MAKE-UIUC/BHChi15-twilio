import os
from flask import Flask, request, redirect, session, make_response
from datetime import datetime, timedelta
import twilio.twiml
#import yaml
import config
import requests
import json



# Configuration
#CONFIG_FILE = 'config.yml'

# Fetch settings from YAML file
#try:
#    with open(CONFIG_FILE, 'r') as f:
#        CONFIG = yaml.load(f)
#except (OSError, IOError) as e:
#    print("Please configure config.yml")
#    exit(1)

SECRET_KEY =  config.key #CONFIG['twilio_secret_key']
GEOCODE_KEY = config.geocode_key

app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    name = request.values.get('Body', None)
    medicine = name.split('near')[0]
    location = name.split('near')[1]
    API_KEY = config.geocode_key
    Address = location 

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
    
    resp = twilio.twiml.Response()
    replyString = medicine + "at apicall(" + latitude + "," + longitude + ")" 
    replyString2 = "To prepay for pickup, text " + "\"" + "XX.XX to order@medsnear.me note XXXXXXX" + "\"" +  "to 729725" 
    replyString3 = "Forward the previous message to a friend if no internet is avaliable, and they are willing to pay for you."    

    resp.message(replyString3)
    resp.message(replyString2)
    resp.message(replyString)
    return str(resp) 
 
if __name__ == "__main__":
    app.run(debug=True)