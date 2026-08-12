from pprint import pprint

def isValidEvent(self, event: dict) -> bool:

    valid = True
    
    if event.get("userId", "null") == "null":

        valid = False
    
    elif event.get("startTimestamp", "null") == "null":

        valid = False
    
    elif event.get("stopTimestamp", "null") == "null":

        valid = False

    else:

        energy = int(event.get("stopValue")) - int(event.get("startValue"))

        if energy < 0:

            valid = False

    if not valid:

        pprint("Invalid event data:")
        pprint(event)

    return valid