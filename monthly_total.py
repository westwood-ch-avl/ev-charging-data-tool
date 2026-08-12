## NB: For the purposes of firestore, this willl be a subcollection under ev_charging_users...

class Monthly_Total:

    year: int
    month: int
    total_wh: int
    num_sessions: int

    def __init__(self, year, month, total_wh, num_sessions):
        self.year = year
        self.month = month
        self.total_wh = total_wh
        self.num_sessions = num_sessions

    def generate_doc_key(self):
        return f"{self.year}-{self.month}"

    def to_dict(self):
        return {
            "year": self.year,
            "month": self.month,
            "total_wh": self.total_wh,
            "num_sessions": self.num_sessions
        }

    @staticmethod
    def from_dict(source):
        return Monthly_Total(
            year=source["year"],
            month=source["month"],
            total_wh=source["total_wh"],
            num_sessions=source["num_sessions"]
        )