from dotenv import load_dotenv
import os
import json
import requests
from event import Event
from ev_charging_user import Ev_Charging_User
from event_error_checker import isValidEvent

from event_error_checker import isValidEvent

load_dotenv()

def initialize_firebase_service_account():
    import firebase_admin
    from firebase_admin import credentials

    key_dict = json.loads(os.environ.get("FIREBASE_DICT"))

    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

##TODO edit this auto-generated code as needed. Need to add params too. Also consider baking in a way to use command line to set how far back to pull events.
def get_powerfill_data() -> list:
    url = os.environ.get("POWERFILL_URL")
    user = os.environ.get("POWERFILL_USER")
    password = os.environ.get("POWERFILL_PASSWORD")

    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from Powerfill: {response.status_code} - {response.text}")

def build_event_list_from_powerfill_list(data) -> list:

    events = []

    for e in data:

        if isValidEvent(e):
            events.append(Event(e["id"], e["startTimeStamp"], e["stopTimeStamp"], e["startValue"],e["stopValue"], e["userId"], e["chargeBoxId"]))

    return events

def get_ev_users_from_db() -> dict:

    import firebase_admin
    from firebase_admin import firestore

    ev_users = {}

    db = firestore.client()
    docs = db.collection("ev-charging-users").stream()

    for doc in docs:
        ev_users[doc.id] = Ev_Charging_User.from_dict(doc.to_dict())

    return ev_users

def post_events_to_db(events: list): #TODO the following is auto generated. Prolly need to fix it. Do these need to be batched? DO I want to store events under each user?

# TODO see this for batching: https://docs.cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.bulk_writer.BulkWriter

    import firebase_admin
    from firebase_admin import firestore

    db = firestore.client()

    for event in events:
        doc_ref = db.collection("events").document(event.generate_doc_key())
        doc_ref.set(event.to_dict())

def do_monthly_totals():

    ... #TODO