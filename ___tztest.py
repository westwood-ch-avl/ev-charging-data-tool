from datetime import datetime
import dateutil

## Converting a "Z" ISO string (UTC) to local timezone


mydatestring = "2024-06-01T12:00:00Z"
mytimezone= "America/New_York"

yourdate = dateutil.parser.parse(mydatestring)

localdate = yourdate.astimezone(dateutil.tz.gettz(mytimezone))

print(localdate.isoformat())  # Output: 2024-06-01T08:00:00-04:00


## COnverting a naive timezone

mydatestring = "2026-02-15T12:00:00"

mydate = dateutil.parser.parse(mydatestring)

mylocaldate2 = mydate.astimezone(dateutil.tz.gettz(mytimezone))
print(mylocaldate2.isoformat())  # Output: 2026-02-15T12:00:00-05:00    