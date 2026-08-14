from datetime import datetime
import dateutil

class Event:

    id: str
    start_time: datetime
    end_time: datetime
    start_wh: int
    end_wh: int
    user_id: int
    charge_box_id: str

    def __init__(self, id, start_time, end_time, start_wh, end_wh, user_id, charge_box_id):
        self.start_time = dateutil.parser.parse(start_time)
        self.end_time = dateutil.parser.parse(end_time)
        self.user_id = user_id
        self.charge_box_id = charge_box_id
        self.start_wh = start_wh
        self.end_wh = end_wh
        self.id = id

    @staticmethod
    def from_dict(source):
        return Event(
            start_time=source["start_time"],
            end_time=source["end_time"],
            user_id=source["user_id"],
            charge_box_id=source["charge_box_id"],
            end_wh = source["end_wh"],
            start_wh = source["start_wh"],
            id = source["id"]
        )

    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "user_id": self.user_id,
            "charge_box_id": self.charge_box_id,
            "start_wh": self.start_wh,
            "end_wh": self.end_wh,
            "id": self.id
        }