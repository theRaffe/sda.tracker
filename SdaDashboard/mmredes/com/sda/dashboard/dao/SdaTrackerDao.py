import sqlite3 as lite
import time
import sys

__author__ = 'macbook'


class SdaTrackerDao:
    'Class for accessing to sqlite database'
    conn = None

    def __init__(self, connectionFile):
        self.conn = lite.connect(connectionFile)

    def get_artifacts(self):
        dict_artifact = {}
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute("select * from cat_artifact")
        rows = cur.fetchall()
        for row in rows:
            key = row["path_directory"]
            value_key = row["code_artifact"]
            dict_artifact[key] = value_key

        return dict_artifact

    def get_list_artifacts(self):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute("select * from cat_artifact")
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append(dict(zip(row.keys(), row)))
        return result

    def get_ticket(self, id_ticket):
        return self.get_ticket(id_ticket, 0)

    def get_ticket(self, id_ticket, id_status):
        self.conn.row_factory = lite.Row
        cur = self.conn.cursor()
        cur.execute("select * from ticket_board where id_ticket = :id_ticket and id_status = :id_status",
                    {"id_ticket": id_ticket, "id_status": id_status})
        return cur.fetchone()

    def update_ticket_board(self, dict_ticket_board):
        cur = self.conn.cursor()
        date_requested = time.time()
        cur.execute(
            "update ticket_board set date_requested = :date_requested, user_request = :user_request where id_ticket = :id_ticket and id_environment = :id_environment",
            {"date_requested": date_requested, "user_request": dict_ticket_board["user_request"],
             "id_ticket": dict_ticket_board["id_ticket"], "id_environment": dict_ticket_board["id_environment"]})
        self.conn.commit()
