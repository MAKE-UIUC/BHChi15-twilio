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
    Address = name 

    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + Address + "&key="+API_KEY)

    jsonResponse = json.loads(r.text)
    try:
        latitude = json.dumps(jsonResponse['results'][0]['geometry']['location']['lat'])
        longitude = json.dumps(jsonResponse['results'][0]['geometry']['location']['lng'])
        replyString = latitude + "," + longitude
    except:
        replyString = "No results found for specified location. Try another description of the location"
    replyString = replyString + medicine + location
    resp = twilio.twiml.Response()
    resp.message(replyString)
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)