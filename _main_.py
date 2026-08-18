from dotenv import load_dotenv
import os
import json
import requests
from event import Event
from ev_charging_user import Ev_Charging_User
from event_error_checker import isValidEvent
from datetime import datetime, date, time
import dateutil
from dateutil.relativedelta import relativedelta
import firebase_admin
import sys

load_dotenv()

def initialize_firebase_service_account():

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

def build_event_dict_from_powerfill_list(data) -> dict:

    events = {}

    for e in data:

        if isValidEvent(e):
            events[e["id"]] = (Event(e["id"], e["startTimeStamp"], e["stopTimeStamp"], e["startValue"],e["stopValue"], e["userId"], e["chargeBoxId"]))

    return events

def get_ev_users_from_db() -> dict:

    from firebase_admin import firestore

    ev_users = {}

    db = firestore.client()
    docs = db.collection("ev-charging-users").stream()

    for doc in docs:
        ev_users[doc.id] = Ev_Charging_User.from_dict(doc.to_dict())

    return ev_users

def post_events_to_db(ev_users: dict, events: list, earliest_date_time:datetime=None):

    from firebase_admin import firestore

    db = firestore.Client()
    bulk_writer = db.bulk_writer()

    bulk_writer.on_write_result(lambda reference, result, bulk_writer: print(f'Saved {reference._document_path}'))

    bulk_writer.on_write_error(lambda bulkwriterfailure, bulk_writer: print(f'Bulk Write Failure: {bulkwriterfailure.message}'))

    for event in events:

        if earliest_date_time:

            if event.start_time < earliest_date_time:
                break

        if event.user_id in ev_users:

            continue

        else:

            new_ev_user = Ev_Charging_User(int(event.user_id), None, datetime.now().astimezone(dateutil.tz.gettz(os.environ.get("TZ"))), None)

            ev_users[str(event.user_id)] = new_ev_user

            ref = db.collection("ev_users").document(str(event.user_id))
            bulk_writer.set(ref, new_ev_user.to_dict())

        doc_ref = db.collection("ev_users").document(str(event.user_id)).collection("events").document(str(event.id))
        bulk_writer.set(doc_ref, event.to_dict())

    bulk_writer.close()

def get_events_from_local_json() -> dict:

    path = os.environ.get("LOCAL_JSON_DATA")

    data = []

    events = {}

    with open(path, 'r') as f:

        data = json.load(f)

    for e in data:

        if isValidEvent(e):

            events[str(e["id"])] = Event(e["id"], e["startTimestamp"], e["stopTimestamp"], e["startValue"], e["stopValue"], e["userId"], e["chargeBoxId"])

    return events

def do_monthly_total(ev_users: dict, specific_date_to_run:date=None):

    ## Figure out the exact start and end of the desired month

    if specific_date_to_run == None:

        specific_date_to_run = date.today() + relativedelta(days=-3)

    start_of_month = datetime.combine(specific_date_to_run, time()).astimezone(dateutil.tz.gettz(os.environ.get("TZ")))
    start_of_month = start_of_month + relativedelta(months=-1, day=1)

    end_of_month = start_of_month + relativedelta(months=+1)

    ## Get the relevant events
    
    from firebase_admin import firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
    
    db = firestore.client()

    query = db.collection_group("events").where(filter=FieldFilter("start_time", ">", start_of_month)).where(filter=FieldFilter("start_time", "<", end_of_month))

    docs = query.stream()

    the_months_events = []

    for doc in docs:

        the_months_events.append(Event.from_dict(doc.to_dict()))

    #post the totals to respective users, using the list of the month's events and the ev_users dict

    #TODO I think I need to make a dict of new "monthly total" objects, one for each user, and then cycle through the events, adding to the totals. Then I need to post those objects.

    for e in the_months_events:

        ... #TODO

def get_command_line_params() -> dict:

    ... # https://realpython.com/command-line-interfaces-python-argparse/#setting-the-type-of-input-values

    ... #TODO should probably pass in separate numbers for how many days to look back for events vs for monthly reports?

if __name__ == "__main__":

    ...