class Chart_Data:

    month: int
    year: int
    wh_table: list
    sessions_table: list

    def __init__(self, month:int, year:int, wh_table:list, sessions_table:list):
        pass

    def generate_key(self) -> str:

        return str(self.year) + str(self.month).zfill(2)

    def to_dict(self) -> dict:

        return {
            "month": self.month,
            "year": self.year,
            "wh_table": self.wh_table,
            "sessions_table": self.sessions_table
        }

    @staticmethod
    def from_dict(source):
        return Chart_Data(source["month"], source["year"], source["wh_table"], source["sessions_table"])

'''The tables should be lists / dicts, sort of like the csv library uses? Column headers are keys...'''

sample_table = [
    {'user_id': "2", "2026-03": "83630", "2026-02": "834600923"},
    {'user_id':"3", "2026-03": "12974"}
] ## etc etc