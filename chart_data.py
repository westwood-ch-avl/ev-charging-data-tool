from datetime import datetime

class Chart_Data:

    date_created: datetime
    wh_table: list
    sessions_table: list

    def __init__(self, date_created: datetime, wh_table:list, sessions_table:list):

        self.date_created = date_created
        self.wh_table = wh_table
        self.sessions_table = sessions_table

    def generate_key(self) -> str:

        return "chart_data"

    def to_dict(self) -> dict:

        return {
            "date_created": self.date_created,
            "wh_table": self.wh_table,
            "sessions_table": self.sessions_table
        }

    @staticmethod
    def from_dict(source):
        return Chart_Data(source["date_created"], source["wh_table"], source["sessions_table"])

'''The tables should be lists / dicts, sort of like the csv library uses? Column headers are keys...'''

sample_table = [
    {'user_id': "2", "2026-03": "83630", "2026-02": "834600923"},
    {'user_id':"3", "2026-03": "12974"}
] ## etc etc