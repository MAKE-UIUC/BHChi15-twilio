import os
from flask import Flask, request, redirect, session, make_response
from datetime import datetime, timedelta
import twilio.twiml
#import yaml
import config



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
#GEOCODE_KEY = CONFIG['geocode_key']

app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    name = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey" + name)
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)