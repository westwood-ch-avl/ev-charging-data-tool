from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

def initialize_firebase_service_account():
    import firebase_admin
    from firebase_admin import credentials

    key_dict = json.loads(os.environ.get("FIREBASE_DICT"))

    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

##TODO edit this auto-generated code as needed. Need to add params too.
def get_powerfill_data():
    url = os.environ.get("POWERFILL_URL")
    user = os.environ.get("POWERFILL_USER")
    password = os.environ.get("POWERFILL_PASSWORD")

    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from Powerfill: {response.status_code} - {response.text}")

def handle_powerfill_data(data):
    ...