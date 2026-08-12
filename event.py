from datetime import datetime

class Event:

    start: datetime
    end: datetime
    user_id: int
    charge_box_id: str

    def __init__(self, start, end, user_id, charge_box_id):
        self.start = start
        self.end = end
        self.user_id = user_id
        self.charge_box_id = charge_box_id

    @staticmethod
    def from_dict(source):
        return Event(
            start=source["start"],
            end=source["end"],
            user_id=source["user_id"],
            charge_box_id=source["charge_box_id"]
        )

    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "user_id": self.user_id,
            "charge_box_id": self.charge_box_id
        }

    def generate_doc_key(self):
        return f"{self.start.isoformat()}-{self.user_id}"