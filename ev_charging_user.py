from datetime import datetime

class Ev_Charging_User:

    unit: str
    user_id: int
    name: str
    created: datetime

    def __init__(self, user_id, name, created, unit):

        self.user_id = user_id
        self.name = name
        self.created = created
        self.unit = unit

    @staticmethod
    def from_dict(source):
        return Ev_Charging_User(
            user_id=source["user_id"],
            name=source["name"],
            created=source["created"],
            unit=source["unit"]
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "created": self.created,
            "unit": self.unit
        }

    def generate_doc_key(self):
        
        return str(self.user_id)